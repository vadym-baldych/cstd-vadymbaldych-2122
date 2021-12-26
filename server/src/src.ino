#define X 3
#define Y 3

#define SYMBOL_E 0
#define SYMBOL_X 1
#define SYMBOL_O 2
#define DRAW_FLAG -1

#define MODE_STATUS_MESSAGE "<server><status>GAME_MODE</status></server>"
#define END_X_STATUS_MESSAGE "<server><status>GAME_END</status><winner>X</winner></server>"
#define END_O_STATUS_MESSAGE "<server><status>GAME_END</status><winner>O</winner></server>"
#define END_DRAW_STATUS_MESSAGE "<server><status>GAME_END</status><winner>DRAW</winner></server>"

#define MODE_COMMAND "MODE"
#define MOVE_COMMAND "MOVE"
#define RESTART_COMMAND "RESTART"

bool gameStarted = false;
int gameMode = 0; // 1 - Man VS Man; 2 - Man VS AI
int currentPlayer = SYMBOL_X;
int gameWinner = 2;
int gameField [3][3] = {{SYMBOL_E, SYMBOL_E, SYMBOL_E},
                        {SYMBOL_E, SYMBOL_E, SYMBOL_E},
                        {SYMBOL_E, SYMBOL_E, SYMBOL_E}};
                        
String getValueXML(String input, String getKey) {
  if (input.indexOf("<" + getKey + ">") > 0){
     int countChar = getKey.length();
     int indexStart = input.indexOf("<" + getKey + ">");
     int indexStop = input.indexOf("</" + getKey + ">");  
     return input.substring(indexStart + countChar + 2, indexStop);
  }
  return "";
}

String gameFieldToXML(int gameField [3][3]) {
  String gameFieldXML = "<gameField>";
  for (int i = 0; i < X; i++) {
    for (int j = 0; j < Y; j++) {
      gameFieldXML += "<cell" + String(i) + String(j) + ">" +
                      String(gameField[i][j]) +
                      "</cell" + String(i) + String(j) + ">";
    }
  }
  gameFieldXML += "</gameField>";
  return gameFieldXML;
}

String gameFieldToClientXML(String sessionID, String clientSide, int gameField [3][3]) {
  String xml_message = "<status>GAME_UPDATE</status>";
  xml_message = "<server>" +
                xml_message +
                "<sessionID>" + sessionID + "</sessionID>" +
                "<currentPlayer>" + clientSide + "</currentPlayer>" +
                gameFieldToXML(gameField) +
                "</server>";
  return xml_message;
}

void updateGameField(int (&gameField)[3][3], int &currentPlayer, String coords, int symbol) {
  int x = String(coords[0]).toInt();
  int y = String(coords[1]).toInt();
  if (gameField[x][y] == SYMBOL_E) {
    gameField[x][y] = symbol;
    if (currentPlayer == SYMBOL_X) {
      currentPlayer = SYMBOL_O;
    }
    else {
      currentPlayer = SYMBOL_X;
    }
  }
}

int checkGameFieldForWinner(int gameField[3][3]) {
  int sameSymbolCounter = 0;
  for (int i = 0; i < 3; i++) {
    if (gameField[i][0] != SYMBOL_E && gameField[i][0] == gameField[i][1] && gameField[i][1] == gameField[i][2]) {
      return gameField[i][0];
    }
    else if (gameField[0][i] != SYMBOL_E && gameField[0][i] == gameField[1][i] && gameField[1][i] == gameField[2][i]) {
      return gameField[0][i];
    }
  }
  if (gameField[1][1] != SYMBOL_E && gameField[0][0] == gameField[1][1] && gameField[1][1] == gameField[2][2]) {
    return gameField[1][1];
  }
  else if (gameField[1][1] != SYMBOL_E && gameField[2][0] == gameField[1][1] && gameField[1][1] == gameField[0][2]) {
    return gameField[1][1];
  }

  bool drawFlag = true;
  for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {
      if (gameField[i][j] == SYMBOL_E) {
        drawFlag = false;
        break;
      }
    }
  }
  if (drawFlag == true) {
    return DRAW_FLAG;
  }
  
  return SYMBOL_E;
}

void startNewGame() {
  ::gameStarted = false;
  ::gameMode = 0;
  ::currentPlayer = SYMBOL_X;
  ::gameWinner = 2;
  for (int i = 0; i < X; i++) {
    for (int j = 0; j < Y; j++) {
      ::gameField [i][j] = SYMBOL_E;
    }
  }
}

void setup() {
  Serial.begin(115200);
}

void loop() {
  String clientMessage = Serial.readString();
  // Game mode
  if (gameStarted == false) {
    Serial.println(MODE_STATUS_MESSAGE);
    if (getValueXML(clientMessage, "status") == MODE_COMMAND) {
      if (gameMode == 0) {
        gameStarted = true;
        gameMode = getValueXML(clientMessage, "mode").toInt();
      }
    }
  }
  else {
    if (getValueXML(clientMessage, "status") == MOVE_COMMAND) {
      if (getValueXML(clientMessage, "player").toInt() == currentPlayer) {
        updateGameField(gameField, currentPlayer, getValueXML(clientMessage, "move"), currentPlayer);
      }
    }
    if (getValueXML(clientMessage, "status") == RESTART_COMMAND) {
      startNewGame();
    }
    Serial.println(gameFieldToClientXML(String("0"), String(currentPlayer), gameField));
    gameWinner = checkGameFieldForWinner(gameField);
    if (gameWinner == SYMBOL_X) {
      Serial.println(END_X_STATUS_MESSAGE);
    }
    else if (gameWinner == SYMBOL_O) {
      Serial.println(END_O_STATUS_MESSAGE);
    }
    else if (gameWinner == DRAW_FLAG) {
      Serial.println(END_DRAW_STATUS_MESSAGE);
    }
  }
}
