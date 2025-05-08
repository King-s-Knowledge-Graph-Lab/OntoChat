"""
Improved Scenario CQ generator – Groups by UNIQUE scenarios or dataset entries.
Sends exactly ONE request per distinct scenario (or dataset when scenario is missing)
and concatenates all Gold‑Standard CQs found for that scenario with "; ".
#uvicorn cq_generator_ontochat_app:app --host 127.0.0.1 --port 8003

"""

from fastapi import FastAPI, File, UploadFile, HTTPException, Response
from gradio_client import Client
from io import StringIO
import pandas as pd, openai, logging, os, time, datetime, pathlib, json

# ─────────────────────────── logging ───────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s │ %(levelname)-8s │ %(message)s",
)
logger = logging.getLogger(__name__)

# ──────────────────────────  clients  ──────────────────────────
ONTOCHAT   = Client("b289zhan/OntoChat")
_OPENAIKEY = os.getenv("OPENAI_API_KEY")

# prime OntoChat **once** with your key
if _OPENAIKEY:
    try:
        ONTOCHAT.predict(_OPENAIKEY, api_name="/set_openai_api_key")
        logger.info("✓ OpenAI key stored in OntoChat session")
    except Exception as e:
        logger.warning(f"Could not set key in OntoChat: {e}")

# ───────────────────── helper functions ───────────────────────
def _prompt_for(scenario: str) -> str:
    return (
        "Here is a user scenario for ontology engineering:\n"
        f"\"\"\"\n{scenario}\n\"\"\"\n\n"
        "Please generate **up to five** competency questions for this scenario "
        "and return them on **one single line, separated by a semicolon** (;)."
    )

HISTORY = [[None,
   ("I am OntoChat, your conversational ontology engineering assistant…")
]]

def _query_ontochat(prompt: str, retry: int = 3, wait: float = 8.0) -> str:
    for attempt in range(1, retry + 1):
        try:
            ans = ONTOCHAT.predict(prompt, HISTORY, api_name="/cq_generator")[0]
            return ans.strip()
        except Exception as e:
            logger.warning(f"OntoChat attempt {attempt}/{retry} failed: {e}")
            if attempt == retry: raise
            time.sleep(wait * attempt)

def _fallback_openai(prompt: str) -> str:
    try:
        resp = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system",
                 "content": "You generate up to five competency questions; "
                            "return them on one line separated by ';'."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=120,
            temperature=0.4,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"OpenAI fallback error: {e}"

# ─────────────────────────── FastAPI ───────────────────────────
app = FastAPI(
    title="Improved Scenario CQ Generator",
    version="2.3.0",
    description="Generates up‑to‑five CQs per UNIQUE scenario or dataset entry.",
)

@app.post("/newapi/")
async def generate_cqs(file: UploadFile = File(...)):
    logger.info(f"★ /newapi/ received {file.filename!r}")

    try:
        content = await file.read()
        df = pd.read_csv(StringIO(content.decode("utf-8")))
        # Keep a copy of the original DataFrame to preserve all rows
        original_df = df.copy()
    except Exception as e:
        raise HTTPException(400, f"CSV read error: {e}")

    # Check available columns in the dataset
    has_scenario_column = "Scenario" in df.columns
    has_cq_column = "Competency Question" in df.columns

    # Determine the main grouping column
    if has_scenario_column:
        logger.info("Using 'Scenario' as primary grouping column")
        grouping_column = "Scenario"
    else:
        # Look ONLY for dataset column
        dataset_columns = [col for col in df.columns if col.lower() not in ["competency question"]
                          and "dataset" in col.lower()]

        if dataset_columns:
            grouping_column = dataset_columns[0]
            logger.info(f"No 'Scenario' column found, using '{grouping_column}' as primary grouping column")
        else:
            raise HTTPException(400, "CSV must contain a 'Scenario' column or a column with 'dataset' in its name")

    # Create a unique key for each row
    # If scenario exists, use it; otherwise use the alternative column
    df["grouping_key"] = df[grouping_column].fillna("").astype(str).str.strip()

    # When grouping key is empty and we have a CQ, use the CQ as the key
    if has_cq_column:
        mask = (df["grouping_key"] == "") & (df["Competency Question"].notna())
        df.loc[mask, "grouping_key"] = "CQ: " + df.loc[mask, "Competency Question"].astype(str).str.strip()

    # Skip completely empty rows (no key and no CQ)
    df = df[df["grouping_key"] != ""]

    # Now group by the unique keys
    groups = df.groupby("grouping_key", dropna=False)

    logger.info(f"Found {len(groups)} unique entries to process")

    # Process each unique group once
    processed_results = {}

    for group_key, group_df in groups:
        # Collect all gold standard CQs for this group
        gold_cqs = []
        if has_cq_column:
            gold_cqs = [str(cq).strip() for cq in group_df["Competency Question"].dropna()
                        if str(cq).strip()]

        gold_combined = " ; ".join(gold_cqs) if gold_cqs else ""

        # If the group key starts with "CQ:", we're using a competency question as the key
        if group_key.startswith("CQ:"):
            prompt_text = group_key[3:].strip()  # Remove the "CQ:" prefix
            logger.info(f"Using CQ as source for generation: [{prompt_text[:40]}...]")
            prompt = _prompt_for(f"Based on this competency question: {prompt_text}")
        else:
            prompt_text = group_key
            logger.info(f"Processing unique entry: [{prompt_text[:40]}...]")
            prompt = _prompt_for(prompt_text)

        # Generate questions
        try:
            generated = _query_ontochat(prompt)
            logger.info(f"✓ CQ(s) generated for: [{prompt_text[:40]}...]")
        except Exception as e:
            if _OPENAIKEY:
                generated = _fallback_openai(prompt)
                logger.info(f"✓ Generated via OpenAI fallback")
            else:
                generated = f"Error generating CQ: {e}"
                logger.error(generated)

        # Store the results for this unique group
        processed_results[group_key] = {
            "gold standard": gold_combined,
            "generated": generated
        }

        # Gentle pacing
        time.sleep(2)

    # Now map the results back to the original DataFrame rows
    results = []

    # For each original row, find its corresponding processed result
    for _, row in original_df.iterrows():
        result_entry = {"gold standard": "", "generated": ""}

        # Determine the grouping key for this row
        if has_scenario_column:
            key = str(row.get("Scenario", "")).strip()
        else:
            key = str(row.get(grouping_column, "")).strip()

        # If key is empty but we have a CQ, use the CQ as key
        if not key and has_cq_column:
            cq = str(row.get("Competency Question", "")).strip()
            if cq:
                key = f"CQ: {cq}"

        # Look up the processed result for this key
        if key in processed_results:
            result_entry = processed_results[key]
        else:
            # If no match, leave empty but record a specific gold standard if available
            if has_cq_column and pd.notna(row.get("Competency Question")):
                result_entry["gold standard"] = str(row["Competency Question"]).strip()
                result_entry["generated"] = "No matching scenario or dataset entry found"

        results.append(result_entry)

    # Create the output DataFrame
    out_df = pd.DataFrame(results)
    logger.info(f"🏁 done – {len(out_df)} rows in the output dataset")

    # Also store the aggregate results (unique groups)
    aggregate_results = []
    for key, data in processed_results.items():
        aggregate_results.append({
            "grouping_key": key,
            "gold standard": data["gold standard"],
            "generated": data["generated"]
        })

    aggregate_df = pd.DataFrame(aggregate_results)

    # Optional JSON dump
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    path = pathlib.Path("results")
    path.mkdir(exist_ok=True)

    # Store both the full results and aggregated results
    (path / f"last_run_{ts}.json").write_text(
        json.dumps(results, indent=2), encoding="utf-8"
    )

    (path / f"last_run_aggregated_{ts}.json").write_text(
        json.dumps(aggregate_results, indent=2), encoding="utf-8"
    )

    # Also save the aggregated CSV file
    (path / f"last_run_aggregated_{ts}.csv").write_text(
        aggregate_df.to_csv(index=False), encoding="utf-8"
    )

    logger.info(f"Saved both full results and aggregated results to 'results' folder")

    return Response(out_df.to_csv(index=False), media_type="text/csv")


# ---------- dev run ----------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("cq_generator_ontochat_app:app",
                host="127.0.0.1", port=8003)