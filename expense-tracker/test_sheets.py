from sheets import GoogleSheetsClient

def test_append_expense():
    client = GoogleSheetsClient()
    test_data = {
        "categorie": "restaurant",
        "fournisseur": "Test Café",
        "date": "2026-06-09",
        "montant_ttc": 12.50,
        "tva": 1.04,
        "devise": "EUR",
        "description": "Ligne de test",
        "confiance": "haute"
    }
    client.append_expense(test_data, image_url=None)
    print("append_expense :ligne ajoutée avec succès")


def test_append_expense_with_image():
    client = GoogleSheetsClient()
    test_data = {
        "categorie": "transport",
        "fournisseur": "SNCF",
        "date": "2026-06-09",
        "montant_ttc": 45.00,
        "tva": 3.75,
        "devise": "EUR",
        "description": "Ligne de test",
        "confiance": "haute"
    }
    fake_url = "https://via.placeholder.com/150"
    client.append_expense(test_data, image_url=fake_url)
    print("append_expense avec image_url : ligne ajoutée avec succès")


if __name__ == "__main__":
    test_append_expense()
    test_append_expense_with_image()
