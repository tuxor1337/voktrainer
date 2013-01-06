Vokabeltrainer für Linux
========================

Vokabeltrainer für Linux geschrieben in Python. Für weitere Informationen, siehe
http://tovotu.de/blog/523-Vokabeltrainer-fr-Linux/ und
http://tovotu.de/dev/517-Vokabeltrainer-fr-Linux-Download--Installation

Schnelleinstieg: Programm in einzelne ausführbare Datei schreiben
-----------------------------------------------------------------

Es ist möglich, eine voll funktionsfähige Version des Programms in eine
ausführbare Datei `dist/voktrainer` zu schreiben. Dazu übergibt man an setup.py
den Befehl `single_file` wie folgt:

    % python setup.py single_file

Installation
------------

Zum Installieren einfach folgenden Befehl ausführen:

    # python setup.py install
    
Für eine Installation ohne Rootrechte den obigen Befehl mit der  Option `--user`
ausführen. Ein beliebiger Zielort für die Installation kann mit der Option
`--root` angegeben werden.

Das Skript bringt leider keine Deinstallationsroutine mit sich. Die erstellten
Dateien müssen daher gegebenenfalls manuell entfernt werden:

    %{platform-prefix}/bin/voktrainer
    %{platform-prefix}/share/applications/voktrainer.desktop
    %{platform-prefix}/share/pixmaps/voktrainer.svg
    %{python-site-packages}/vok/
    %{python-site-packages}/Vokabeltrainer_f_r_Linux-1.0-py2.7.egg-info
    
`%{python-site-packages}` und `%{platform-prefix}` hängen vom Betriebssystem ab.
In Fedora werden diese Werte Standardmäßig auf
`/usr/lib/python2.7/site-packages` bzw. `/usr` gesetzt.

Für weitere Informationen, siehe

    $ python setup.py install --help

License
-------

This program is free software; you can redistribute it and/or modify it under
the terms of VERSION 2 of the GNU General Public License as published by the
Free Software Foundation provided that the above copyright notice is included.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.

Go to http://www.gnu.org/licenses/gpl-2.0.html to get a copy of the license.
