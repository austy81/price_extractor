# Price Extactor (aka Price robot)

## Poslání
Program má z daných url načíst ceny produktů.

## Detaily
Seznam adres musí být uložený v podadresáři excel soubor in.xlsx.

Soubor musí obsahovat dvě záložky:
1. Tab s názvem url obsahuje adresy, ze kterých chceme získat ceny
2. Tab s názvem settings obsahuje sloupce v tomto pořadí:
    - url regex
        - obsahuje regulární výraz pro rozpoznání url adresy (zde lze testovat: https://regex101.com/)
    - price element
        - obsahuje XPath výraz pro získání elementu ceny ze stránky (popis např. zde: https://aka.ms/Jmnqsv)
    - verify exists
        - XPath výraz, který je vyhledán na stránce a pokud tam není, pak napíše chybu
        - Chyba: Element which should exsist was not found
    - verify not exists
        - to samé jako předchozí akorát naopak
        - takže pokud element existuje skončí s chybou
        - Chyba: Found element which should not exist
    - parser - určuje jakým způsobem se bude cena získávat
        - selenium (komplexní process co spotřebovává hodně prostředků a funguje jako prohlížeč)
        - requests (rychlejší ale nefunguje pro všechny stránky)


## Chyby
* No parser - Nenašel parser, který odpovídá dané adrese v záložce settings [modrá]
* Error opening url - Stránka je nedostupná [fialová]
* Element which should exsist was not found - našel element který na stránce nemá být [žlutá]
* Found element which should not exist - nenašel element který by tam měl být
* Error finding price on page - nenašel element s cenou
* Error parsing price - v elementu kde má být cena nenašel čísla
* Error parsing page - nějaká chyba ve zpracování html stránky