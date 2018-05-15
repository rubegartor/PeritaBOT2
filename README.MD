# PeritaBOT 2


**PeritaBOT 2** es una nueva versión mejorada del antiguo [PeritaBOT](https://github.com/rubegartor/PeritaBOT). Con este bot de discord proporcionaras nuevos comandos a tus usuarios, entre los que destacan comandos administrativos, miscelánea, Music Bot, etc.

# Comandos
Todos los comandos del bot los puedes encontrar en la siguiente lista:

|Comandos                 |Descripción                                             |Permisos     |
|-------------------------|--------------------------------------------------------|-------------|
|`8ball [pregunta]`       |La bola mágica responde a tus preguntas                 |Usuario      |
|`memes help`             |Más información sobre el grupo de comandos              |Usuario      |
|`space [num] [word]`     |Añade num espacios entre las letras de la palabra       |Usuario      |
|`reverse [text]`         |Da la vuelta al contenido del mensaje                   |Usuario      |
|`avatar [username(s)]`   |Obtiene la foto de perfil de los usuarios mencionados   |Usuario      |
|`ping`                   |Muestra la latencia (ms) del bot                        |Usuario      |
|`overwatch [username#id]`|Información sobre el jugador en Overwatch               |Usuario      |
|`osu [username]`         |Información sobre el jugador en Osu!                    |Usuario      |
|`random [max_num]`       |Devuelve un número aleatorio                            |Usuario      |
|`react [text]`           |Reacciona al último mensaje del canal en forma de emojis|Usuario      |
|`choose [opciones]`      |Elige una opción entre todas                            |Usuario      |
|`cat`                    |Muestra una foto aleatoria de gatos                     |Usuario      |
|`dog`                    |Muestra una foto aleatoria de perros                    |Usuario      |
|`help`                   |Muestra el mensaje de ayuda                             |Usuario      |
|`info`                   |Muestra información sobre el servidor y el Bot          |Usuario      |
|`updates`                |Muestra si hay actualizaciones disponibles              |Usuario      |
|`invite`                 |Genera la URL de invitación para PeritaBOT 2            |Usuario      |
|`spamvoice [channel]`    |Spamea el canal de voz que especifiques                 |Usuario      |
|`se [emoji]`             |Muestra la imagen original de un emoji                  |Usuario      |
|`summon`                 |Une al bot a tu canal de voz                            |Usuario      |
|`join [channel]`         |Une al bot al canal de voz especificado                 |Usuario      |
|`playing`                |Muestra la cancion que se esta reproduciendo            |Usuario      |
|`skip`                   |Peticion para saltar la cancion actual                  |Usuario      |
|`play [url] or [title]`  |Reproduce/agrega la cancion especificada                |Usuario      |
|`pause`                  |Pausa la cancion actual                                 |Usuario      |
|`resume`                 |Continua la cancion pausada                             |Usuario      |
|`volume [0-100]`         |Establece el volumen para la musica                     |Usuario      |
|`stop`                   |Kickea el bot del canal de voz                          |Usuario      |
|`mute [username]`        |Mutea al usuario del canal de voz                       |Administrador|
|`unmute [username]`      |Desmutea al usuario del canal de voz                    |Administrador|
|`ban [username]`         |Banea al usuario del servidor                           |Administrador|
|`unban [username]`       |Desbanea al usuario del servidor                        |Administrador|
|`ban_list`               |Muestra la lista de usuarios baneados en el servidor    |Administrador|
|`spam [msg]`             |Spammea un mensaje 10 veces por un canal de texto       |Administrador|
|`prune [num]`            |Elimina num de mensajes (Max. 99)                       |Administrador|

# Configuración
En esta nueva versión se ha mejorado el modo de configuración del bot ya que tan solo tendremos que editar un archivo *config.ini* con la configuración necesaria.

    [PeritaBOT]
    token=Ezk5NTc0Onm83hjliPDI0MjAy.DbJ-nQ.IBtH0vEC_lkorkEKuwWOssq7
    rootRole=bot
    prefix=!
    [ChronoGG]
    channel=18874298390634752
    hour=18
    [Osu]
    osu=d4b2d8c20786a997e0a5b90f143c7530
    [Memes]
    path=/home/PeritaBOT/memes/

**[PeritaBOT]** - Configuración básica del bot

 - **token**: Podemos encontrar el token de nuestro bot en el siguiente enlace: [Discord Bot Token](https://discordapp.com/developers/applications/me)
 - **rootRole**: Este es el nombre del rango administrativo superior del servidor

 ![enter image description here](https://i.imgur.com/XFyf7sd.png)

 - **prefix**: Es el prefijo utilizado delante de los comandos del bot.
 ***Ejemplo***: *!help*

**[ChronoGG]** -Configuración de las notificaciones de ChronoGG

 - **channel**: Id del canal donde queremos que envie las notificaciones
 - **hour**: Hora a la que queremos que envie la notificación al canal de texto

**[Osu]** - Configuración de Osu

 - **osu**: Token de la API de osu, podemos encontrar nuestro token de osu en: [Osu API Token](https://osu.ppy.sh/p/api)

**[Memes]** - Configuración de los Memes

 - **path**: Ruta a la carpeta que contiene los memes
    - *Linux:* /home/PeritaBOT/memes/
    - *Windows:* C:\\\Usuarios\\\PeritaBOT\\\Escritorio\\\memes\\\

# Instalación
Para instalar la librería principal del bot:

    python3 -m pip install -U discord.py[voice]

Para instalar otras librerías de python3 necesarias:

    python3 -m pip install -r requirements.txt

Para instalar el paquete ffmpeg:

    sudo apt-get install ffmpeg
