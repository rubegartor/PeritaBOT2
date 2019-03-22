# PeritaBOT 2


**PeritaBOT 2** es una nueva versión mejorada del antiguo PeritaBOT. Con este bot de discord proporcionaras nuevas utilidades a tu servidor.

# Comandos
Todos los comandos del bot los puedes encontrar en la siguiente lista:

|Comandos                 |Descripción                                             |Permisos      |
|-------------------------|--------------------------------------------------------|--------------|
|`help`                   |Muestra el mensaje de ayuda                             |everyone      |
|`8ball [pregunta]`       |La bola mágica responde a tus preguntas                 |everyone      |
|`avatar [username(s)]`   |Obtiene la foto de perfil de los usuarioss mencionados  |everyone      |
|`osu [username]`         |Información sobre el jugador en Osu!                    |everyone      |
|`react [text]`           |Reacciona al último mensaje del canal en forma de emojis|everyone      |
|`se [emoji]`             |Muestra la imagen original de un emoji                  |everyone      |
|`game [user]`            |Empieza el juego Conecta 4 con el jugador especificado  |everyone      |
|`PCCom help`             |Muestra más información sobre el comando PCCom          |everyone      |
|`PCCom list`             |Muestra una lista de las páginas disponibles            |everyone      |
|`PCCom show`             |Muestra la ayuda para utilizar el comando               |everyone      |
|`mute [username]`        |Mutea/desmutea al usuario del canal de voz              |root_role     |
|`deaf [username]`        |Ensordece al usuario del canal de voz                   |root_role     |
|`prune [username]`       |Banea al usuario del servidor                           |root_role     |

# Configuración
La configuración del archivo `config.json` debería parecerse al siguiente:

    {
      "PeritaBOT": {
        "token":"Ezk5NTc0Onm83hjliPDI0MjAy.DbJ-nQ.IBtH0vEC_lkorkEKuwWOssq7",
        "rootRole":"bot",
        "prefix":"!",
        "cogs": ["cogs.core", "cogs.mod", "cogs.pccom", "cogs.osu", "cogs.4inrow"]
      },
      "Osu": {
        "osu":"d4b2d8c20786a997e0a5b90f143c7530"
      }
    }

**[PeritaBOT]** - Configuración básica del bot

 - **token**: Podemos encontrar el token de nuestro bot en el siguiente enlace: [Discord Bot Token](https://discordapp.com/developers/applications/me)
 - **rootRole**: Este es el nombre del rango administrativo superior del servidor

 ![RoleExample](https://i.imgur.com/XFyf7sd.png)

 - **prefix**: Es el prefijo utilizado delante de los comandos del bot.
 ***Ejemplo***: *!help*

**[Osu]** - Configuración de Osu

 - **osu**: Token de la API de osu, podemos encontrar nuestro token de osu en: [Osu API Token](https://osu.ppy.sh/p/api)

# Instalación
Para instalar la librería principal del bot:

    pip install -U git+https://github.com/Rapptz/discord.py@rewrite#egg=discord.py

Para instalar otras librerías de python3 necesarias:

    pip install -r requirements.txt