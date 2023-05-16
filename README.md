# Analiza danych strumieniowych z użyciem uczenia maszynowego

## Zbiór danych

Kickstarter to popularna platforma crowdfundingowa, która pomogła tysiącom przedsiębiorców i twórców urzeczywistnić swoje innowacyjne pomysły. Niemniej jednak, nie wszystkie projekty na Kickstarterze odnoszą sukces, a zrozumienie czynników wpływających na sukces lub porażkę może być cenne zarówno dla twórców, jak i inwestorów.

W tym zbiorze danych zebrane zostały informacje na temat dużej liczby projektów Kickstartera i tego, czy ostatecznie udało im się osiągnąć zamierzone cele finansowe. Zestaw danych obejmuje szeroki zakres typów projektów, w tym startupy technologiczne, twórcze projekty artystyczne i inicjatywy o wpływie społecznym.

Zbiór danych ma rozmiar 49,2 MB, jest w formacie `.csv`, składa się z 374853 wierszy oraz następujących kolumn:

| Nazwa Kolumny | Opis |
| --- | --- |
| ID | Unikalny identyfikator projektu |
| Name | Nazwa projektu |
| Category | Główna kategoria, do której należy projekt |
| Subcategory | Podkategoria, do której należy projekt |
| Country | Kraj pochodzenia produktu |
| Launched | Data rozpoczęcia projektu |
| Deadline | Ostateczny termin na zebranie środków |
| Goal | Kwota pieniędzy, której twórca potrzebuje, aby zakończyć projekt (USD) |
| Pledged | Kwota pieniędzy zadeklarowana przez społeczność (USD) |
| Backers | Liczba osób wspierających projekt |


Źródło: [https://www.kaggle.com/datasets/ulrikthygepedersen/kickstarter-projects](https://www.kaggle.com/datasets/ulrikthygepedersen/kickstarter-projects)

## Folder "preparation"

Skrypt "prepare_dataset.py" przygotowuje zbiór kickstarter_projects.csv poprzez usunięcie niepotrzebnych kolumn, koduje zmienne jakościowe do postaci binanej. Także służy do testowania modeli.

### Wyniki modeli:

- LogisticRegression: 0.69
- MLP (PCA = 100, hidden layers = 10, 5): 0.70
- LogisticRegression (zbiór wraz z kolumną "Backers"): 0.87
