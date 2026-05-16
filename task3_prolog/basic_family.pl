% Task 3(b) – Basic Prolog Family Tree Logic Tests
% Foundations of Artificial Intelligence

%  Facts: parent(Parent, Child) 
parent(tom, bob).
parent(tom, liz).
parent(bob, ann).
parent(bob, pat).

%  Facts: male/female 
male(tom).
male(bob).
male(pat).
female(liz).
female(ann).

%  Rules 

% Father: a male parent
father(X, Y) :- parent(X, Y), male(X).

% Mother: a female parent
mother(X, Y) :- parent(X, Y), female(X).

% Grandparent: parent of a parent
grandparent(X, Z) :- parent(X, Y), parent(Y, Z).

% Sibling: share the same parent (and are not the same person)
sibling(X, Y) :- parent(P, X), parent(P, Y), X \= Y.

%  How to Run Basic Tests 
% Open SWI-Prolog, load this file with:
%   ?- consult('basic_family.pl').

