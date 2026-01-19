from network.game import Game
from network.player import Player
from serverConfig import ServerConfig
import asyncio
from constantStrings import ConstantStrings

async def main(): 
    print(ConstantStrings.GREETING)
    
    ans = ""    
    while ans not in ["1", "2"]:
        print(ConstantStrings.CHOOSE_VALUE) 
        ans = input()

    if ans == "1": 
        host = ServerConfig.host
        port = ServerConfig.port
        
        game_instance = Game(
            host, 
            port
        )

        print(
f"""
host: {host}
port: {port}
"""
        )
        # player_id = input("Введите ваш username\n")
        # player = Player(
        #     player_id, 
        #     host, 
        #     int(port) # тут проблема в том, что нужно менять EndGameState.py для того, чтобы все соо по очереди приходили
        # )
    if ans == "2": 
        player_id = input("Введите ваш username\n")
        
        # host = input("Введите IP хоста: \n")
        # port = input("Введите port хоста: \n")
        
        host = ServerConfig.host
        port = ServerConfig.port
        
        player = Player(
            player_id, 
            host, 
            int(port)
        )

    await asyncio.Future()
if __name__ == "__main__": 
    asyncio.run(main())