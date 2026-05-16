% Includes: grandparents, parents, children, grandchildren,
%           cousins, uncles and aunts
% Foundations of Artificial Intelligence

% FACTS  parent(Parent, Child)


% Grandparents → Parents
parent(james, david).
parent(james, susan).
parent(james, robert).
parent(mary, david).
parent(mary, susan).
parent(mary, robert).

parent(george, linda).
parent(george, peter).
parent(grace, linda).
parent(grace, peter).

% Parents → Children
parent(david, alice).
parent(david, brian).
parent(linda, alice).
parent(linda, brian).

parent(robert, charlie).
parent(robert, diana).
parent(susan, charlie).    % susan married into this branch
parent(susan, diana).

% FACTS – Gender

male(james).
male(george).
male(david).
male(robert).
male(peter).
male(brian).
male(charlie).

female(mary).
female(grace).
female(susan).
female(linda).
female(alice).
female(diana).

% RULES

% Father: a male who is a parent
father(X, Y) :-
    parent(X, Y),
    male(X).

% Mother: a female who is a parent
mother(X, Y) :-
    parent(X, Y),
    female(X).

% Grandparent: parent of a parent
grandparent(X, Z) :-
    parent(X, Y),
    parent(Y, Z).

% Grandfather: a male grandparent
grandfather(X, Z) :-
    grandparent(X, Z),
    male(X).

% Grandmother: a female grandparent
grandmother(X, Z) :-
    grandparent(X, Z),
    female(X).

% Grandchild: inverse of grandparent
grandchild(X, Z) :-
    grandparent(Z, X).

% Sibling: two people who share a parent
sibling(X, Y) :-
    parent(P, X),
    parent(P, Y),
    X \= Y.

% Brother: a male sibling
brother(X, Y) :-
    sibling(X, Y),
    male(X).

% Sister: a female sibling
sister(X, Y) :-
    sibling(X, Y),
    female(X).

% Uncle: a male sibling of a parent
uncle(X, Y) :-
    parent(P, Y),
    brother(X, P).

% Aunt: a female sibling of a parent
aunt(X, Y) :-
    parent(P, Y),
    sister(X, P).

% Cousin: children of siblings
cousin(X, Y) :-
    parent(PX, X),
    parent(PY, Y),
    sibling(PX, PY),
    X \= Y.

% HOW TO RUN – Example Queries
%
%   ?- consult('my_family_tree.pl').
%
% Then try these queries:
%
% Who are james's grandchildren?
%   ?- grandchild(Who, james).
%
% Is alice a grandchild of james?
%   ?- grandchild(alice, james).
%
% Who are alice's uncles?
%   ?- uncle(Who, alice).
%
% Who are alice's aunts?
%   ?- aunt(Who, alice).
%
% Who are alice and brian's cousins?
%   ?- cousin(alice, Who).
%
% Who are the grandparents?
%   ?- grandparent(Who, _), !.
%
% List all cousins:
%   ?- cousin(X, Y).

