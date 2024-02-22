# Music Knowledge

## Persona

Linka is a researcher in Computer Science.

## Goal
*Keywords: music data, multi-modal data, knowledge discovery*

Linka is interested in finding and describing music-related data of heterogeneous types and formats from different sources. Thanks to the ability to represent diverse content, her main goal is to inter-relate music data so as to enable large scale experiments for knowledge discovery.


## Scenario

Linka is carrying out a lot of manual work to find music data on the Web from different datasets, catalogues, platforms and services. In addition, all this data needs to be carefully inspected so that information retrieved from a certain source is matched to that of another source, in a consistent manner. Although this can be done for a few musical objects of interest (e.g. information related to an album), the analytical and manual process becomes unmanageable and tremendously time-consuming when the scope of the analysis increases (e.g. hundreds of songs). In turn, this jeopardises the possibility of conducting large scale computational studies, which are fundamental for knowledge discovery -- establishing links among musical objects and entities to unveil novel relationships[^1].

Thanks to Polifonia, Linka will be able to perform all the aforementioned operations in an automatic manner and with little supervision. Starting from some desiderata -- names of artists, composers, musical pieces, albums -- the system will attempt to find pertinent music-related data from a specific set of resources (see below). Besides the computational requirements of the system for finding relevant content, this requires to semantically describe the retrieved data. 



## Example Data

For simplicity, music-related data can be categorised as: cataloguing information, musical features, musical facts, and musical relationships.

**Cataloguing information**

Information needed to identify a musical work as well as its relationships with the recordings that are derived from it. For example:
- "Penny Lane" is a musical work by "The Beatles",
- "Penny Lane" was composed by "John Lennon" and "Paul McCartney";
- The first recording of "Penny Lane" was released in February 1967 as a double A-side single with "Strawberry Fields Forever".

Linka is interested in tracing the basic discographic information associated to the recordings of a certain musical work, including: the year of release, the name of the release, the place of recording, the instruments/performers relationships, and the vocals. Example data to address this category can be found from [MusicBrainz] and [Wikidata].

- The specific track of "Penny Lane" featured in the album "Strawberry Fields Forever" was recorded in "Abbey Road Studios: Studio 2" in "St John's Wood, Westminster, London (UK)" on 1966-12-29, 1967-01-05, 1967-01-06, 1967-01-09, and 1967-01-17.
- The album "Strawberry Fields Forever" has been originally released in the UK on 1967-02-17.
- The background and lead vocals of "Penny Lane" are by "Paul McCartney".
- The "tambourine" is played by "Ringo Starr".


**Musical features**

Musical features can range from simple tags associated with a musical work or a recording (e.g. genre, style) to the tonality, tempo, and lyrics of the piece. Music tags are generally provided by all databases mentioned in the Resources section below; tonality and tempo are given by [Wikidata] and [MusicBrainz] through [AcousticBrainz][-2]; lyrics are provided by [Genius] and [SongFacts]. Please, note that Linka aims at modelling lyrics at the sentence level (bottom level) and also at the sectional level (top level). This last consideration is not fully captured by the example reported below, although the data provided by [Genius] and [SongFacts] allows for this organisation.

- The musical work "Penny Lane" has genres/style "baroque pop" and "psychedelic pop".
- The "original mono studio mix" of "Penny Lane" featured in "Strawberry Fields Forever" is in B minor (tonality = key + scale) and its tempo is 115 BPM.
- The (original) lyrics of "Penny Lane" are "In Penny Lane there is a barber showing photographs + "\n" + Of every head he's had the pleasure to know ..."

**Musical facts**

These are usually considered as textual explanations of the lyrics (e.g. "Four of fish and finger pies" in "Penny Lane" is explained by Genius as a "common order size for fish and chips, that is what you could get with four pence..."), curiosities on the composition process (e.g. "The piquant trumpet part was added after the rest of the song was finished."), pertinent artist-related facts (e.g. "Lennon's mother Julia at one time worked as a cinema usher and a waitress in Penny Lane."), but also relationships to places and their meaning in the lyrics (e.g. "Penny Lane, Liverpool, England"). These can be found from [Genius] and [SongFacts].


**Musical relationships**

Establishing connections among pieces and recordings based on objective and/or subjective criteria and musical properties. These include derivative works (e.g. covers, medleys, mesh-ups), and sampling relationships where a certain musical pattern -- originally set/induced in a musical work, is found in other pieces. Examples of the former can be found from [SecondHandSongs] and [MusicBrainz], whereas [WhoSampled] provides data for the latter.

- "Penny Lane" is referred to in the following medleys: "A Liverpool Day", "She's leaving home / Penny Lane" and "The Music of the Beatles".
- "Penny Lane" was translated in Finnish with "Rööperiin".
- An instrumental version of "Penny Lane" was released by Al Di Meola in September 2013.
- "Penny Lane" was covered by "Kai Warner" in 1976.
- "Penny Lane" was sampled by "The Rutles" in "Doubleback Alley". The sample appears at 1:16, 1:35, 1:43, and 2:35, corresponding to  1:12, 1:27, 1:33, and 2:41 in the original performance.

## Data resources

An example of music-related data for the same song (Penny Lane) is given below.

* MusicBrainz: https://musicbrainz.org/work/1548c8c0-108f-33a8-9671-a025aa68e382
* Wikidata: https://www.wikidata.org/wiki/Q842168
* Genius: https://genius.com/1376466
* SongFacts: https://www.songfacts.com/facts/the-beatles/penny-lane
* SecondHandSongs: https://secondhandsongs.com/work/8937/
* WhoSampled: https://www.whosampled.com/The-Beatles/Penny-Lane/

[MusicBrainz]: https://musicbrainz.org/work/1548c8c0-108f-33a8-9671-a025aa68e382
[Wikidata]: https://www.wikidata.org/wiki/Q842168
[Genius]: https://genius.com/1376466
[SongFacts]: https://www.songfacts.com/facts/the-beatles/penny-lane
[SecondHandSongs]: https://secondhandsongs.com/work/8937/
[WhoSampled]: https://www.whosampled.com/The-Beatles/Penny-Lane/


[^1] This use case is the specific scope of another story: Linka#2 (coming soon).

[-2] AcousticBrainz will be shut down (news from Mid-Feb 2022).
