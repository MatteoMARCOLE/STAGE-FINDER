def normaliser_offre_france_travail(offre):
    entreprise = offre.get("entreprise") or {}
    lieu_travail = offre.get("lieuTravail") or {}
    origine_offre = offre.get("origineOffre") or {}

    return {
        "id_offre": f"france_travail:{offre.get('id')}",
        "titre": offre.get("intitule"),
        "entreprise": entreprise.get("nom"),
        "lieu": lieu_travail.get("codePostal"),
        "contrat": offre.get("typeContrat"),
        "description": offre.get("description"),
        "date_creation": offre.get("dateCreation"),
        "url": origine_offre.get("urlOrigine"),
        "source": "france_travail",
    }


def normaliser_offre_adzuna(offre):
    entreprise = offre.get("company") or {}
    lieu = offre.get("location") or {}

    return {
        "id_offre": f"adzuna:{offre.get('id')}",
        "titre": offre.get("title"),
        "entreprise": entreprise.get("display_name"),
        "lieu": lieu.get("display_name"),
        "contrat": offre.get("contract_type"),
        "description": offre.get("description"),
        "date_creation": offre.get("created"),
        "url": offre.get("redirect_url"),
        "source": "adzuna",
    }


def normaliser_offre_jooble(offre):
    return {
        "id_offre": f"jooble:{offre.get('id')}",
        "titre": offre.get("title"),
        "entreprise": offre.get("company"),
        "lieu": offre.get("location"),
        "contrat": offre.get("type"),
        "description": offre.get("snippet"),
        "date_creation": offre.get("updated"),
        "url": offre.get("link"),
        "source": "jooble",
    }
