"""
General-purpose SPARQL queries

"""

NE_QUERY = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>

    SELECT DISTINCT ?individual ?other
    WHERE {
        ?individual rdf:type owl:NamedIndividual ;
        rdf:type ?other .
        FILTER ( ?other not in ( owl:NamedIndividual ) )
    }
    """
