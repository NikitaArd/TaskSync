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
    - [Wymagania systemowe](#wymagania-systemowe)
    - [Krok po kroku](#krok-po-kroku)
    - [Po instalacji](#uwagi)
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
Jest to projekt na konkurs informatyczny PCKZiU w Wieliczce.  
Strona internetowa służy do wspólnego organizowania i wykonywania projektów szkolnych, lub własnych. 


</br>

---

</br>

#### <a id='opis-techniczny'></a> :page_with_curl: Opis techniczny
Językiem programowania wystąpił **Python**, ze względu na swoją czytelność i ogromną bazę bibliotek.   
Fundamentem projektu jest Python Framework do tworzenia aplikacji internetowych, **Django**.  
Do przechowywania danych była wybrana baza danych **PostgreSQL**.
Także chcę zwrócić uwagę na to ze została użyta przez mnie biblioteka **channels** (Potrzebna do nawiązywania i obsługi dwukierunkowego połączenia), ponieważ był to dla mnie pierwsze doświadczenie z tą technologią.

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

[Oryginał](https://drawsql.app/teams/nikita-5/diagrams/dnd-desk)  

![Struktura](https://i.ibb.co/m5730Vv/Zrzut-ekranu-2022-12-5-o-20-58-50.png)

---

</br>

## <a id='jak-zbudować'></a> :computer: Jak zbudować projekt lokalnie ?

</br>

### <a id='wymagania-systemowe'></a> Wymagania systemowe

Aby zbudować projekt lokalnie, na komputerze mają być zainstalowane:

 > Python 3.x
https://www.python.org/

 > PostgreSQL
https://www.postgresql.org/

</br>

### <a id='krok-po-kroku'></a> Krok po kroku

1. Pobrać folder z projektem, lub za pomocą wiersz poleceń
```
git clone https://github.com/NikitaArd/django-project-manager
```
</br>

 2. W tym folderze
 ```
 python -m venv venv
 ```
 Lub
 ```
 python3 -m venv venv
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

 5. Stworzyć bazę danych PostgreSQL
 ```
 python db_creator.py django_project_manager <hasło> <host> <port>
 ``` 
 *Podpowiedź !*  
 *Domyślne hasło root*  
 *Domyślny host 127.0.0.1*  
 *Domyślny port 5432*

</br>

 6. Stworzyć strukturę bazy danych
 ```
 cd project_manager

 python manage.py migrate
 ```

 </br>

7. Stworzyć konto Administratora (By mieć dostęp do panelu administratora)
 ```
 python manage.py createsuperuser
 ```

</br>

 8. Włączyć lokalny server !
 ```
 python manage.py runserver
 ```

 </br>

## <a id='uwagi'></a> Uwaga !

Po przygotowaniu projektu, trzeba dodać minimalnie 1 zdjęcie profilowe w panelu administratora. Inaczej stworzenia konta użytkownika będzie **niemożliwe**.

1. Przejdź do panelu administratora i zaloguj się jako administrator

![Krok 1](https://i.ibb.co/vJfkDL9/Zrzut-ekranu-2022-12-8-o-23-11-44.png)

2. Znajdź na liście model Avatarów

![Krok 2](https://i.ibb.co/7WrwwnC/Zrzut-ekranu-2022-12-8-o-23-12-04.png)

3. Kliknij dodaj avatar

4. Dodaj zdjęcie i wypełni pole wyszukiwania (slug_avatar_1)

![Krok 4](https://i.ibb.co/BzZB2xw/Zrzut-ekranu-2022-12-8-o-23-14-32.png)

5. Zapisz zmiany

6. Gotowe !
