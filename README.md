# Analiza danych strumieniowych z użyciem uczenia maszynowego

## Folder "preparation"

Skrypt "prepare_dataset.py" przygotowuje zbiór kickstarter_projects.csv poprzez usunięcie niepotrzebnych kolumn, koduje zmienne jakościowe do postaci binanej. Także służy do testowania modeli.

### Wyniki modeli:

- LogisticRegression: 0.69
- MLP (PCA = 100, hidden layers = 10, 5): 0.70
- LogisticRegression (zbiór wraz z kolumną "Backers"): 0.87

