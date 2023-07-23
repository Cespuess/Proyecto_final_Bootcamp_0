# Simulador de criptomonedas

Prototipo de aplicación web realizada con flask sin seguridad ni gestión de usuarios.
Permite registrar compras simuladas de ciertas criptomonedas:
- **_EUR_**     - ADA       - BNB       - BTC       - DOT
- ETH       - MATIC     - SOL       - USDT      - XRP

## Reglas básicas de la simulación de compra-venta
1. Se dispone de una cantidad ilimitada de euros.
2. Con euros solo se podrá comprar BTC, y seguido con BTC cualquier criptomoneda, y cualquier criptomoneda entre ellas.
3. Se podrá vender cualquier criptomoneda directamente a euros.
4. Sólo se podrá vender una criptomoneda si se dispone de saldo de la misma. 

## Funcionalidad de la aplicación
Dispone de tres pantallas básicas:
* Pantalla "Mis Movimientos": Contiene el resumen con todos los movimientos (compra-venta) realizados.
* Pantalla "Trading": Es en la que realizaremos la compra-venta de criptomonedas.
* Pantalla "Wallet: Mostrará el estado de la inversión. Podremos ver las cantidades y su valor en euros de las criptomonedas que dispongamos, el valor actual de la suma de todas, el valor en euros que se pagaron por ellas y el resultado de la inversión.

## Instalación

### Servicios externos

Se utiliza coinAPI.io como servicio para calcular el valor actual de cada criptomoneda. Será necesario solicitar una apikey en [su web](https://www.coinapi.io/market-data-api/pricing)

### Pasos a seguir para utilizar el programa

1. Replicar el fichero "env.template" y renombrarlo ".env"
2. Informar las siguientes claves:
    - FLASK_APP: main.py (no modificar)
    - FLASK_DEBUG: en entornos de producción debe ser False, si se va a modificar la aplicación es más cómodo True
    - FLASK_SECRET_KEY: introducir una clave secreta cualquiera. Una buena web para generarlas es [randomkeygen](https://randomkeygen.com).
    - FLASK_PATH_SQLITE: Aquí pondremos el path del fichero sqlite donde se grabarán los movimientos, o si se desea dejar como está.
    - FLASK_API_KEY: la apikey de coinAPI.io que habremos obtenido más [arriba](#servicios-externos). 

## Ejecución de la aplicación

1. Instalar todas las dependencias:
    - Abrir la terminal y escribir lo siguiente:
    ```
    pip install -r requirements.txt
    ```

2. Lanzar la aplicación desde directorio donde esté instalada la aplicación:
    ```
    flask run
    ```