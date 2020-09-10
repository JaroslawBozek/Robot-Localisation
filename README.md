# lokalizacja

1. Inicjalizacja<br/>
W inicjalizacji przygotowywana jest macierz self.P o wymiarach 4xlocations. Posiada ona prawdopodobieństwo
znalezienia się robota na każdym polu z każdą możliwą orientacją.

2. Uwzględnienie poprzedniej akcji<br/>
Na początku funkcji __call__ tworzona jest macierz out_T o wymiarach 4xlocationsxlocations.
W przypadku gdy robot poruszy się naprzód, owa macierz przechowuje informację o mnożniku
prawdopodobieństwa znalezienia się na danym polu. Jeśli robot poruszył sięd o przodu to
kolejne pole otrzymuje mnożnik 0.95, a aktualne 0.05.<br/>
W przypadku kiedy robot się obrócił w lewo lub prawo, program operuje na macierzy self.P.<br/>
Podczas obrotu w prawo, prawdopodobieństwa odpowiedniego kierunku przyjmują wartości:<br/>
current_direction = (1-eps_move) * left_direction + eps_move * current_direction.<br/>
Wartości 0.95 oraz 0.05 oczywiście wynikają z szansy na to, że robot się nie obróci.

3. Uwzględnienie informacji z sensorów<br/>
Macierz self.out_O o wymiarach 4xlocations posiada informację o zgodności aktualnych odczytów z 
sensora z każdym możliwym położeniem i orientacją robota na mapie.
W przypadku zgodnego odczytu wynik mnożony jest *0.9, a w przypadku niezgodnego *0.1.


4. Następna akcja<br/>
Wynika z odczytów pozycji robota na mapie. Każda pozycja bierze pod uwagę sąsiadujące z nią ściany. Jeśli przykładowo szansa na niewystąpienie ściany przed robotem będzie wynosić 80% to będzie mieć on 80% szansy na ruch do przodu i 20% szansy na skręcenie.


5. Aktualizacja rozkładu prawdopodobieństw<br/>
W funkcji getPosterior() aktualizowana jest macierz self.P poprzez wymnażanie nowych odczytów z tymi, które
są już uwzględnione w macierzy self.P<br/>
Dane te są także odpowiednio przeliczane na P_arr, aby móc je zwizualizować na mapie.

