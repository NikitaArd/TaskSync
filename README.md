## Django Project Manager  

---

### :anchor: Spis treści

- [:clipboard: Wprowadzenie](#wprowadzenie)
    - [Opis](#opis)
    - [Opis techniczny](#opis-techniczny)
    - [Kontrola wersji](#kontrola-wersji)
- [:electric_plug: Dane techniczne](#dane-techniczne)
    - [Główne narzędzia](#główne-narzędzia)
    - [Biblioteki](#biblioteki)
    - [Struktura bazy danych](#struktura)
- [:computer: Jak zbudować projekt lokalnie ?](#jak-zbudować)
</br>
</br>
</br>
</br>
</br>
</br>
</br>

## <a id='wprowadzenie'></a> :clipboard: Wprowadzenie
---

</br>

#### <a id='opis'></a> :scroll: Opis
Jest to projekt na konkurs informatyczny PCKZiU w Wieliczkce.  
Strona internetowa słuzy do wspólnego organizowania i wykonywania projektór szkolych, lub własnych. 

</br>

---

</br>

#### <a id='opis-techniczny'></a> :page_with_curl: Opis techniczy
Językiem programowania wystąpił **Python**, ze względu na swoją czytelność i ogromną bazę bibliotek.   
Fundamentem projektu jest Python Framework do tworzenia aplikacji internetowych, **Django**.  
Do przechowywania danych była wabrana baza danych **PostgreSQL**.
Takze chcę zwrócić uwagę na to ze została uzyta przez mnie biblioteka **channels** (Potrzebna do nawiązywania i obsługi dwukierunkowego połączenia), poniewaz był to dla mnie pierwsze doświatczenie z tą technologią.

</br>

---

</br>

## <a id='kontrola-wersji'></a> :seedling: Kontrola Wersji

### **Przykład**

    [1.2.3.4] Zawartość commit'a . . .

*1* - Zmiany, które są **widoczne** użytkowniku    
*2* - Zmiany, które są **nie widoczne** użytkowniku  
*3* - Zmiany ustawień  
*4* - Naprawa błędów

### Jeśli wersja się nie zmieniła, kod projektu został bez zmian.

</br>

---

</br>

## <a id='dane-techniczne'></a> :electric_plug: Dane techniczne 

| <a id='główne-narzędzia'></a>Główne narzędzia |  |
| ----------- | ----------- |
| Język programowania | :snake: Python |
| Framework | :gun: Django |
| Baza danych | :elephant: PostgreSQL |
| Edytor tekstu | :wrench: Vim |

---


| <a id='biblioteki'></a>Biblioteki |  |
| ----------- | ---------- |
| Django | 4.1.3 |
| Django widget tweaks | 1.4.12 |
| Psycopg2 | 2.9.5 |
| Channels | 3.0.5 |
| Pillow | 9.3.0 |

*Biblioteki które trzeba instalować ręcznie*   

</br>


---
### <a id='struktura'></a> Struktura bazy danych

</br>

[Orginał](https://drawsql.app/teams/nikita-5/diagrams/dnd-desk)  

![Struktura](https://i.ibb.co/m5730Vv/Zrzut-ekranu-2022-12-5-o-20-58-50.png)

---

</br>

## <a id='jak-zbudować'></a> :computer: Jak zbudować projekt lokalnie ?

Krok po kroku

1. Pobrać folder z projektem, lub za pomocą wiersz poleceń
```
git clone https://github.com/NikitaArd/django-project-manager
```
</br>

 2. W tym folderze
 ```
 python -m venv venv
 ```
</br>

 3. Aktywować python venv 
 ```
 Unix:
 source venv/bin/activate

 Windows:
 venv/scripts/activate
 ```

</br>

 4. Zainstalować wszystkie biblioteki
 ```
 cd django-project-manager

 pip install -r requirements.txt
 ```

</br>

 5. Stworzyć baze danych PostgreSQL
 ```
 python db_creator.py django_project_manager <hasło> <host> <port>
 ``` 
 *Uwaga !*  
 *Domyślne hasło root*  
 *Domyśny port 127.0.0.1*  
 *Domyśny port 5432*

</br>

 6. Stworzyć strukturę bazy danych
 ```
 cd project_manager

 python manage.py migrate
 ```

 </br>

(Opcjonalne)  
7. Stworzyć Administratora (By mieć dostęp do panelu administratora)
 ```
 python manage.py createsuperuser
 ```

</br>

 8. Włączyć lokalny server !
 ```
 python manage.py runserver
 ```

