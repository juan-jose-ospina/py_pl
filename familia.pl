% familia.pl - Base de conocimiento de ejemplo para consultar desde Python.

% dynamic permite agregar/quitar hechos desde Python (assertz/retract).
:- dynamic progenitor/2, hombre/1, mujer/1.

% --- Hechos: progenitor(Padre_o_Madre, Hijo) ---
progenitor(juan, maria).
progenitor(juan, pedro).
progenitor(ana, maria).
progenitor(ana, pedro).
progenitor(maria, lucia).
progenitor(maria, carlos).
progenitor(pedro, sofia).

% --- Hechos: género ---
hombre(juan).
hombre(pedro).
hombre(carlos).
mujer(ana).
mujer(maria).
mujer(lucia).
mujer(sofia).

% --- Reglas ---
padre(X, Y) :- progenitor(X, Y), hombre(X).
madre(X, Y) :- progenitor(X, Y), mujer(X).

hermano(X, Y) :-
    progenitor(P, X),
    progenitor(P, Y),
    X \= Y.

abuelo(X, Y) :- progenitor(X, Z), progenitor(Z, Y).

ancestro(X, Y) :- progenitor(X, Y).
ancestro(X, Y) :- progenitor(X, Z), ancestro(Z, Y).

% Regla con cálculo aritmético.
factorial(0, 1) :- !.
factorial(N, F) :-
    N > 0,
    N1 is N - 1,
    factorial(N1, F1),
    F is N * F1.
