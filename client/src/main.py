from connection import *
from game import *
from player import *
from minimax import *
from db import *
import time

player = Player()
game = Game()

while True:
    game.update()
    player.update(game)
    
    while True:
        try:
            game.server_message_xml = get_serial_message(SERVER_ROOT["start"], SERVER_ROOT["end"], game.server_message_xml)
            game.server_message_dict = xml_to_dict(game.server_message_xml)
            break
        except Exception as e:
            if str(e)[:14] == "ClearCommError":
                pygame.quit()
                message_box("Error", "Can't find Arduino COM port.", 1)
                sys.exit()
            continue

    # Choose game mode
    if game.server_message_dict["status"] == "GAME_MODE":
        game.draw_menu()
        game.draw_statistics()
    # Get game field
    elif game.server_message_dict["status"] == "GAME_UPDATE":
        game.current_player = int(game.server_message_dict["currentPlayer"])
        game.parse_game_field(game.server_message_dict["gameField"])
        game.draw_game_field()
    elif game.server_message_dict["status"] == "GAME_END":
        game.game_winner = game.server_message_dict["winner"]
        game.write_statistics()
        game.draw_game_field()
        game.draw_game_winner()

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and game.game_status == True:
            if game.server_message_dict["status"] == "GAME_MODE":
                if game.man_vs_man_rect.collidepoint(player.mouse_position):
                    game.game_mode = 1
                    choose_mode_message = game.genenerate_mode_command()
                    if time.time() - game.last_send_message_time > game.TIMEOUT_TIME:
                        game.last_send_message_time = time.time()
                        send_serial_message(choose_mode_message)
                        game_session = GameSession(1, db_cursor)
                        game_session.write_session()
                if game.man_vs_ai_rect.collidepoint(player.mouse_position):
                    game.game_mode = 2
                    ai_enemy = PlayerRepresentation(1)
                    ai = PlayerRepresentation(2)
                    choose_mode_message = game.genenerate_mode_command()
                    if time.time() - game.last_send_message_time > game.TIMEOUT_TIME:
                        game.last_send_message_time = time.time()
                        send_serial_message(choose_mode_message)
                        game_session = GameSession(2, db_cursor)
                        game_session.write_session()
            else:
                if game.server_message_dict["status"] == "GAME_END":
                    if game.restart_rect.collidepoint(player.mouse_position):
                        restart_message = game.gen_restart_xml()
                        if time.time() - game.last_send_message_time > game.TIMEOUT_TIME:
                            game.last_send_message_time = time.time()
                            send_serial_message(restart_message)
                            game_session.update_session(game.game_winner)
                elif player.grid_x != -1 and player.grid_y != -1:
                    if game.game_mode == 1:
                        move_message = player.generate_move_command(game)
                        if time.time() - game.last_send_message_time > game.TIMEOUT_TIME:
                            game.last_send_message_time = time.time()
                            send_serial_message(move_message)
                            game_session.write_turn(game.current_player_symbol, player.session_position)
                    elif game.game_mode == 2:
                        if game.current_player == game.SYMBOL_X:
                            move_message = player.generate_move_command(game)
                            if time.time() - game.last_send_message_time > game.TIMEOUT_TIME:
                                game.last_send_message_time = time.time()
                                send_serial_message(move_message)
                                game_session.write_turn(game.current_player_symbol, player.session_position)
                        elif game.current_player == game.SYMBOL_O:
                            ai_turn = ai.get_decision(numpy.array(game.game_field), ai_enemy)
                            move_message = player.generate_move_command_ai(game, ai_turn)
                            if time.time() - game.last_send_message_time > game.TIMEOUT_TIME:
                                game.last_send_message_time = time.time()
                                send_serial_message(move_message)
                                game_session.write_turn(game.current_player_symbol, player.session_position)
            
        if event.type == pygame.QUIT: 
            sys.exit()
    
    pygame.display.update()