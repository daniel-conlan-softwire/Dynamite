interface GameState {
  rounds: Round[];
}

interface Round {
  p1: string;
  p2: string;
}

class Bot {
  dynamiteCount: number;
  enemyDynamiteCount: number;
  currentStrategy: Bot;
  allStrategies: Bot[];
  availableMoves: string[];
  rollover: number;
  scoreDifference: number;

  constructor() {
    this.dynamiteCount = 99;
    this.enemyDynamiteCount = 100;
    this.allStrategies = [new RandomBot(), new CopyLastMoveBot(), new BeatLastMoveBot(), new HMMBot()];
    this.currentStrategy = this.allStrategies[0];
    this.availableMoves = ["R", "P", "S", "W", "D"];
    this.rollover = 0;
    this.scoreDifference = 0;
  }

  updateAvailableMoves( // TODO: rename
    movePlayedLastRound: string,
    enemyMovePlayedLastRound: string,
  )  {

    this.availableMoves = ["R", "P", "S", "W", "D"];

    if (movePlayedLastRound === "D") {
      this.dynamiteCount -= 1;
    }

    if (enemyMovePlayedLastRound === "D") {
      this.enemyDynamiteCount -= 1;
    }

    if (this.dynamiteCount === 0) {
      this.availableMoves = this.availableMoves.filter((m) => m !== "D");
    }

    if (this.rollover < 1 || this.enemyDynamiteCount < 40) { // TODO: this is a threshold to be set
        this.availableMoves = this.availableMoves.filter((m) => m !== "W");
    } 
  }

  pickRandomFrom(array: (string|Bot) []): any { // TODO: implement some weights (could be static or dynamic)
    return array[Math.floor(Math.random() * array.length)];
  }

  switchStrategy() {
    if (this.scoreDifference >= 50) { // TODO: this is a threshold to be set (make obvious we are losing 50) (implement round buffer) (use number of consecutive loses instead)
        this.currentStrategy = this.pickRandomFrom(this.allStrategies); // TODO: exclude the current strategy
    }
  }

  makeMove(gamestate: GameState): string {

    this.switchStrategy();

    if (gamestate.rounds.length > 0) {
      const lastRound = gamestate.rounds[gamestate.rounds.length - 1];
      this.updateAvailableMoves(lastRound.p1, lastRound.p2);
    }
    return this.currentStrategy.makeMove(gamestate);
  }
}

class RandomBot extends Bot {

  makeMove(gamestate: GameState): string {
    return this.pickRandomFrom(this.availableMoves);
  }

}

class CopyLastMoveBot extends Bot {

makeMove(gamestate: GameState): string {
    return gamestate.rounds[gamestate.rounds.length - 1].p2;
}

}

class BeatLastMoveBot extends Bot {

    getMovesThatBeat(move:string): string[] {
        switch (move) {
            case 'R' :
                return ['P', 'D'];
            case 'P' :
                return ['S', 'D'];
            case 'S' : 
                return ['R', 'D'];
            case 'W' : 
                return ['R', 'P', 'S'];
            case 'D' : 
                return ['W'];
            default :
                return ['R', 'P', 'S', 'W', 'D'];
        }
    }

    makeMove(gamestate: GameState): string {
        
        const lastMove = gamestate.rounds[gamestate.rounds.length-1].p2;
        const movesThatBeat = this.getMovesThatBeat(lastMove).filter((m) => this.availableMoves.includes(m));

        if (movesThatBeat.length > 0) {
            return this.pickRandomFrom(movesThatBeat);
        }

        return this.pickRandomFrom(['R', 'P', 'S']);
    }
}

class HMMBot extends Bot {
    
}

module.exports = new Bot()
