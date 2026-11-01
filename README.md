# Cours Radioamateur

Application multiplateforme (Android, Windows, macOS, Linux) de lecture du
cours **« Préparation au certificat d'opérateur du service amateur »** rédigé
par **F6GPX** pour le **Radio-Club de la Haute Île (F6KGL / F5KFF)**, édition
de novembre 2025.

Réalisée en C++17, Qt 6 (6.4 ou plus récent) et QML. L'application fonctionne
entièrement hors ligne et ne demande aucune autorisation.

## Fonctionnalités

- Le cours complet : introduction, réglementation (R-1 à R-5), technique
  (chapitres 0 à 12) et annexes, avec un sommaire qui descend jusqu'aux
  signets de paragraphe de l'original (par exemple `T-1.7d`) et des renvois
  internes cliquables.
- Tous les schémas, graphiques et tableaux dessinés en vectoriel natif
  (184 figures qui étaient des images dans le PDF ont été redessinées, en plus
  des dessins vectoriels du PDF) : nets à tous les niveaux de zoom et
  recolorés pour le thème sombre. Seules les photographies et la carte des
  régions UIT restent des images.
- Texte adaptatif : les paragraphes se réorganisent selon la largeur de
  l'écran (téléphone ou ordinateur), taille du texte réglable (80 % à 160 %).
  Le texte est justifié quand les lignes sont assez longues, aligné à gauche
  sur les écrans étroits.
- Thèmes clair et sombre.
- Visionneuse de schémas avec zoom (pincement, Ctrl + molette, double appui).
- Reprise de la lecture là où vous l'aviez laissée.

## Installation

Les paquets de chaque version sont publiés dans la page **Releases** du dépôt
GitHub.

| Système | Fichier |
|---|---|
| Android 9 ou plus récent (ARM 64 bits) | `CoursRadio-<version>-arm64_v8a.apk` |
| Windows 10/11, installateur | `CoursRadio-<version>-win64-setup.exe` |
| Windows 10/11, portable (sans installation) | `CoursRadio-<version>-win64-portable.zip` |
| macOS 12 ou plus récent (Apple Silicon et Intel) | `CoursRadio-<version>-macos.dmg` |
| Linux, toutes distributions x86_64 | `CoursRadio-<version>-x86_64.AppImage` |
| Ubuntu 24.04 / 26.04 | `coursradio_<version>_ubuntu24.04_amd64.deb` / `..._ubuntu26.04_amd64.deb` |
| Debian 12 / 13 | `coursradio_<version>_debian12_amd64.deb` / `..._debian13_amd64.deb` |

- **Android** : ouvrez le fichier APK sur le téléphone et autorisez
  l'installation depuis cette source si Android le demande.
- **Windows** : lancez l'installateur, ou décompressez l'archive portable et
  lancez `CoursRadio.exe`. Les programmes non signés peuvent déclencher un
  avertissement SmartScreen (« Informations complémentaires » puis
  « Exécuter quand même »).
- **macOS** : ouvrez l'image disque et glissez l'application dans le dossier
  Applications. L'application n'est pas signée par un compte développeur
  Apple : au premier lancement, faites un clic droit sur l'application puis
  « Ouvrir », ou exécutez
  `xattr -dr com.apple.quarantine "/Applications/CoursRadio.app"`.
- **Linux (AppImage)** : `chmod +x CoursRadio-*.AppImage` puis lancez le
  fichier. Qt est inclus dans l'AppImage.
- **Debian / Ubuntu** : prenez le paquet de votre version, puis
  `sudo apt install ./coursradio_<version>_<distribution>_amd64.deb`.
  Le paquet utilise les bibliothèques Qt 6 de la distribution, installées
  automatiquement par apt.

## Crédits et licence

Le contenu du cours appartient à **F6GPX** et au **Radio-Club de la Haute
Île** (<https://f6kgl-f5kff.fr>) et il est publié sous la licence
[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).
Cette application en est une adaptation et elle est distribuée sous la même
licence, pour un usage non commercial. Voir [LICENSE.md](LICENSE.md) pour le
détail et pour les composants tiers (polices Liberation et DejaVu, Qt).

Application : CoursRadio Community.

## Compilation

Le numéro de version est défini à un seul endroit, dans `CMakeLists.txt`
(`project(CoursRadio VERSION x.y.z)`) ; tous les scripts le lisent là. Les
paquets sont écrits dans `dist/`.

### Debian 12+ et Ubuntu 24.04+ (Qt 6 de la distribution)

```bash
./build_linux.sh --install-deps   # installe les dépendances de compilation (sudo), puis compile
./build_linux.sh --run            # compile et lance l'application
./make_deb.sh                     # compile et crée dist/coursradio_<version>_<distribution>_amd64.deb
sudo apt install ./dist/coursradio_1.0.0_ubuntu24.04_amd64.deb
```

Le paquet `.deb` contient uniquement l'application, son entrée de menu, ses
icônes et ses métadonnées AppStream. Il est construit pour la distribution
sur laquelle `make_deb.sh` est lancé : les dépendances vers les bibliothèques
Qt sont calculées par `dpkg-shlibdeps` (leurs noms diffèrent d'une version à
l'autre, par exemple `libqt6core6` sur Debian 12 et `libqt6core6t64` sur
Ubuntu 24.04) et le nom du fichier indique la distribution.

### Linux : AppImage

```bash
QT_DIR=~/Qt/6.8.3/gcc_64 ./build_appimage.sh    # crée dist/CoursRadio-<version>-x86_64.AppImage
```

Le script télécharge [linuxdeploy](https://github.com/linuxdeploy/linuxdeploy)
et son greffon Qt, puis inclut dans l'AppImage les bibliothèques Qt, les
modules QML et les greffons nécessaires. Sans `QT_DIR`, il utilise le Qt du
système (trouvé par `qmake6`). Pour qu'elle fonctionne sur le plus grand
nombre de distributions, compilez l'AppImage sur un système ancien (la
publication automatique utilise Ubuntu 22.04).

### Windows 10/11

Prérequis :

- Visual Studio 2022 avec la charge de travail *Développement Desktop en C++*
  (compilateur, CMake et Ninja) ;
- Qt 6.4 ou plus récent, kit MSVC 64 bits (installateur en ligne de Qt) ;
- Inno Setup 6.3 ou plus récent.

Depuis l'**invite de commandes x64 Native Tools for VS 2022** :

```bat
build_windows.bat
```

Le script utilise le kit MSVC 64 bits le plus récent présent dans `C:\Qt`
(par exemple `C:\Qt\6.11.2\msvc2022_64`). Définissez `QT_ROOT` si Qt est
installé ailleurs, ou `QT_DIR` pour choisir un kit.

Résultats :

- `dist\CoursRadio-<version>-win64\` : dossier portable (application,
  bibliothèques Qt déployées par `windeployqt`, bibliothèques d'exécution
  MSVC copiées à côté de l'exécutable) ;
- `dist\CoursRadio-<version>-win64-setup.exe` : installateur (français et
  anglais, entrée dans le menu Démarrer, raccourci sur le bureau en option,
  désinstallation).

`build_windows.bat noinstaller` ne crée pas l'installateur. `ISCC` permet
d'indiquer un autre emplacement d'Inno Setup.

### macOS

Prérequis : Xcode (outils en ligne de commande), CMake, Qt 6.4 ou plus récent
(installateur en ligne de Qt).

```bash
cmake -S . -B build-macos -DCMAKE_BUILD_TYPE=Release -DCMAKE_PREFIX_PATH=~/Qt/6.8.3/macos
cmake --build build-macos --parallel
~/Qt/6.8.3/macos/bin/macdeployqt build-macos/CoursRadio.app -qmldir=qml
codesign --force --deep --sign - build-macos/CoursRadio.app
```

Ajoutez `-DCMAKE_OSX_ARCHITECTURES="arm64;x86_64"` pour une application
universelle (Apple Silicon et Intel). La signature ad hoc (`--sign -`) est
nécessaire sur Apple Silicon après le passage de `macdeployqt`.

### Android

Prérequis (système Linux) : Qt 6.4 ou plus récent installé avec
l'installateur en ligne de Qt, avec le composant **Android** (par exemple
`android_arm64_v8a`) et le composant **Desktop** de la même version, le SDK
Android, la version du NDK recommandée pour votre version de Qt, et le JDK 17.

```bash
./build_android.sh
adb install -r dist/CoursRadio-1.0.0-arm64_v8a.apk
```

Le script utilise la version de Qt la plus récente présente dans `~/Qt` qui a
le kit Android (par exemple `~/Qt/6.11.2/android_arm64_v8a` avec
`~/Qt/6.11.2/gcc_64`) et le SDK de `$ANDROID_HOME` ou `~/Android/Sdk`. Ces
choix peuvent être modifiés avec `QT_ROOT`, `QT_ANDROID`, `QT_HOST`,
`ANDROID_SDK_ROOT` et `ANDROID_NDK_ROOT` ; `ANDROID_ABI` choisit une autre
architecture (`armv7`, `x86_64`, `x86`).

Sans fichier de clés, l'APK est signé avec la clé de débogage Android, ce qui
suffit pour l'installer sur un appareil. Pour une signature de publication,
définissez `QT_ANDROID_KEYSTORE_PATH`, `QT_ANDROID_KEYSTORE_ALIAS`,
`QT_ANDROID_KEYSTORE_STORE_PASS` et `QT_ANDROID_KEYSTORE_KEY_PASS`.

Le manifeste Android et les icônes de lancement sont dans `packaging/android/`
(nom de paquet `org.coursradio.app`).

## Publication d'une version (GitHub Actions)

Le workflow [`.github/workflows/release.yml`](.github/workflows/release.yml)
compile l'application pour tous les systèmes et publie les paquets dans une
release GitHub `v<version>` sur la branche `main` :

| Tâche | Machine | Résultat |
|---|---|---|
| Android | Ubuntu 24.04, Qt 6.8 pour Android, NDK r26b | APK arm64-v8a |
| Windows | Windows Server 2022, Qt 6.8 MSVC 2022, Inno Setup | installateur et archive portable |
| macOS | macOS 14, Qt 6.8 (universel) | image disque `.dmg` |
| AppImage | Ubuntu 22.04, Qt 6.8 | AppImage x86_64 |
| Deb | conteneurs Ubuntu 24.04, Ubuntu 26.04, Debian 12 et Debian 13, Qt de chaque distribution | quatre paquets `.deb`, installés pour vérification |

La release contient aussi `SHA256SUMS.txt` (sommes de contrôle de tous les
fichiers), un tableau des fichiers par système et les notes de version
générées automatiquement par GitHub.

Pour publier une version :

1. mettez à jour la version dans `CMakeLists.txt`
   (`project(CoursRadio VERSION 1.1.0 ...)`) et poussez sur `main` ;
2. lancez le workflow, au choix :
   - depuis l'onglet **Actions** > **Release** > **Run workflow**, sur la
     branche `main` (options : brouillon, préversion) ;
   - en poussant l'étiquette correspondante : `git tag v1.1.0 && git push origin v1.1.0`
     (le workflow refuse une étiquette qui ne correspond pas à la version de
     `CMakeLists.txt`).

La version de Qt utilisée pour Android, Windows, macOS et l'AppImage est
définie par `QT_VERSION` au début du workflow.

**Signature de l'APK** : sans configuration, l'APK est signé avec une clé de
débogage créée à chaque exécution ; pour mettre à jour l'application, il faut
alors la désinstaller d'abord. Pour signer avec une clé de publication
permanente, ajoutez ces secrets au dépôt (*Settings* > *Secrets and
variables* > *Actions*) :

- `ANDROID_KEYSTORE_BASE64` : le fichier de clés encodé en base64
  (`base64 -w0 release.keystore`) ;
- `ANDROID_KEYSTORE_PASSWORD` : le mot de passe du fichier de clés ;
- `ANDROID_KEY_ALIAS` : l'alias de la clé ;
- `ANDROID_KEY_PASSWORD` : le mot de passe de la clé.

## Organisation du projet

```
CMakeLists.txt          projet CMake Qt 6 (module QML « CoursRadio »)
src/                    C++ : moteur de rendu des schémas, éléments QML, contenu, réglages
qml/                    interface (accueil, sommaire, lecture des chapitres, visionneuse de schémas)
content/course/         chapitres du cours (JSON, un fichier par chapitre, et index.json)
content/figures/        schémas au format vectoriel natif (JSON)
content/images/         les quelques photographies conservées en image
fonts/                  Liberation Serif / Sans (mêmes métriques que les polices du PDF)
                        et CoursRadio Symbols (extrait de DejaVu pour les symboles qui leur manquent)
icons/                  icônes de l'interface et de l'application
packaging/              ressources et installateur Windows, fichiers Linux, icône macOS, manifeste Android
tools/                  chaîne de production (Python) qui crée content/ à partir du PDF
.github/workflows/      publication automatique des versions
build_linux.sh, make_deb.sh, build_appimage.sh, build_windows.bat, build_android.sh
```

## Format des schémas

Les schémas sont de petits documents JSON d'opérations de dessin exprimées en
points PDF (tracés avec contour, remplissage, pointillés et extrémités ;
textes avec indices et exposants, styles, rotation et alignement ; images).
Le format est décrit au début de [`src/diagram.h`](src/diagram.h). Le même
moteur de rendu sert à l'application et à l'outil d'aperçu `figrender`
(`cmake -DCOURSRADIO_BUILD_TOOLS=ON`).

En thème sombre, chaque couleur garde sa teinte et voit sa luminosité
inversée entre la couleur du papier et celle de l'encre : les schémas restent
lisibles sans version sombre séparée.

## Chaîne de production du contenu (mainteneurs)

Les fichiers de `content/` sont générés à partir du PDF original, qui ne fait
pas partie de ce dépôt : téléchargez-le sur <https://f6kgl-f5kff.fr> et
indiquez son chemin dans `COURSRADIO_PDF`.

Prérequis : Python 3, PyMuPDF et Pillow (`pip install pymupdf pillow`) ; les
aides à la mesure utilisent aussi OpenCV et Tesseract.

```bash
export COURSRADIO_PDF=/chemin/vers/cours_radio.pdf
python3 tools/extract_course.py     # chapitres, paragraphes, tableaux, dessins vectoriels
python3 tools/build_figures.py      # remplace les figures en image par leurs dessins natifs
```

- `tools/extract_course.py` convertit le texte (paragraphes, titres,
  signets, soulignements, tableaux) et les dessins vectoriels, et garde une
  copie brute de chaque figure dans `tools/build/rawfigs/`. Les corrections
  manuelles sont dans `tools/course_overrides.json` (`replace` : remplacements
  de texte ; `drop` : paragraphes retirés, comme le plan du livre d'exercices
  à la fin de l'introduction).
- `tools/figures/*.py` contiennent les dessins natifs des figures qui étaient
  des images dans le PDF, écrits avec le petit langage de dessin de
  `tools/figdsl.py` (une fonction par figure, enregistrée avec
  `@figure("cPPP_N#i")`).
- `tools/build_figures.py` substitue ces dessins et signale les figures qui
  restent à dessiner (`tools/build/todo.json`).
- `tools/raster_sheet.py compare <clé>...` affiche l'original et le dessin
  côte à côte pour vérification ; `tools/look.py`, `tools/measure.py`,
  `tools/trace.py` et `tools/contour.py` aident à mesurer les originaux. Ils
  écrivent dans `build-work/` et utilisent l'outil `figrender` compilé avec
  `cmake -S tools/figrender -B build-figrender && cmake --build build-figrender`
  (ces emplacements se changent avec `COURSRADIO_WORK` et
  `COURSRADIO_FIGRENDER`).
- `tools/check_course.py` vérifie que chaque mot du PDF se retrouve dans les
  chapitres ou dans les schémas, sauf dans les paragraphes retirés
  volontairement (`drop`).
- `tools/make_symbol_font.py` recrée `fonts/CoursRadioSymbols.ttf` à partir de
  DejaVu Sans ; `tools/make_icons.py` recrée les icônes (interface,
  application, Windows, macOS, Android).

## Limites connues

- Avec le moteur de rendu *logiciel* de Qt Quick (`QT_QUICK_BACKEND=software`,
  utilisé seulement sur les machines sans OpenGL, Direct3D ni Vulkan), Qt 6.4
  peut dessiner un soulignement parasite dans les paragraphes qui contiennent
  des mots soulignés. Les moteurs de rendu accélérés ne sont pas concernés.
