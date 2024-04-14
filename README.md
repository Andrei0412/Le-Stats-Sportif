Simiocencu Andrei 341C2

## Organizare

* Urmand sugestiile din scheletul oferit am ajuns la aceasta implementare finala, in sectiunea "Implementare" voi da mai multe detali.
* Avand in vedere ca nu prea am folosit la alte materi python mi s-a parut ca tema a fost utila pentru aprofundarea conceptelor din python.
* Am optimizat cat de mult am stiut, asa ca sunt de parere ca e o implementare destul de eficienta, dar probabil se poate mai bine.


## Implementare
* Am implementat toate cerintele.
* In ceea ce priveste structura si flow-ul programului, acesta functioneaza in urmatorul mod: Se primeste un request iar in routes se face preluarea datelor si se paseaza datele necesare ThreadPool-ului care are o coada de task-uri partajata cu toti workerii lui. Workerii verifica ce fel de task au primit si apeleaza functia corespunzatoare din DataIngestor, aceasta clasa contine toate functiile si variabilele necesare pentru a lucra cu fisierul csv si pentru a face calculele necesare. Atunci cand se primeste shutdown, ThreadPool-ul este notificat si seteaza o variabila pe false, astfel incat atunci cand metoda add_task e apelata cu un task acesta nu va fi adaugat. De asemenea aceasta variabila este partajata si de catre workeri, astfel incat atunci cand variabila este setata pe False iar coada este goala, acestia stiu sa se opreasca.
* In ceea ce priveste dificultatile intampinate, acestea ar fi procesarea jsoanelor rezultate asa cum erau in ref-uri, probleme cu import-uri, si folosirea structurilor de date din python si a functionalitatilor pandas.


## Resurse utilizate
* Ocw-ul de asc.
* Documentatia pandas.
* https://reqbin.com pentru request-uri.
* Alte site-uri si tutoriale video(cum ar fi pentru logger).


## Github
* https://github.com/Andrei0412/Le-Stats-Sportif


