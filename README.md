# lokalizacja

1. Inicjalizacja
W inicjalizacji przygotowywana jest macierz self.P, o wymiarach 4x42. Posiada ona prawdopodobieństwo
znalezienia się robota na każdym polu i z każdą orientacją.

2. uwzględnienie poprzedniej akcji
Na początku funkcji __call__ tworzona jest macierz out_T o wymiarach 4x42x42.
W przypadku gdy robot poruszy się naprzód, owa macierz przechowuje informację o mnożniku
prawdopodobieństwa znalezienia się na danym polu. Jeśli robot poruszył sięd o przodu to
kolejne pole otrzymuje mnożnik 0.95, a aktualne 0.05.

W przypadku kiedy robot się obrócił w lewo lub prawo, program operuje na macierzy self.P.
Podczas obrotu w prawo, prawdopodobieństwa odpowiedniego kierunku przyjmują wartości:

current_direction = 0.95 * left_direction + 0.05 * current_direction.
Wartości 0.95 oraz 0.05 oczywiście wynikają z szansy na to, że robot się nie obróci.

3. uwzględnienie informacji z sensorów
Macierz self.out_O o wymiarach 4x42, posiada informację o zgodności aktualnych odczytów z 
sensora, z każdym możliwym położeniem i orientacją robota na mapie.
W przypadku zgodnego odczytu wynik mnożony jest *0.9, a w przypadku niezgodnego *0.1.


4. Następna akcja
Wynika ona bezpośrednio z odczytów z sensora. Jeśli pole przed robotem jest wolne, rusza on do przodu. 
Jeśli nie jest wolne, to sprawdza czy odczyt na lewo/prawo jest ścianą. Jeśli tak to wykonuje obrót w przeciwnym
do odczytu kierunku. Jeśli wszystkie trzy odczyty wykrywają ścianę to wykonuje obrót w lewo.


5. Aktualizacja rozkładu prawdopodobieństw.
W funkcji getPosterior() aktualizowana jest macierz self.P poprzez wymnażanie nowych odczytów z tymi, które
są już uwzględnione w macierzy self.P
Dane te są także odpowiednio przeliczane na P_arr, aby móc je zwizualizować na mapie.

