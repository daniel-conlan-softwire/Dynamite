class beatLastMoveBot {

    dynamiteCount: number;

    constructor() { 
        this.dynamiteCount = 100;
    }

    pickRandomFrom(array: string[]) {
        return array[Math.floor(Math.random() * array.length)];
    }

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

    makeMove(gamestate: any) {

        let choice;

        if (gamestate.rounds.length === 0) {
            choice = this.pickRandomFrom(['R', 'P', 'S', 'W', 'D']);
        } else {

            const lastMove = gamestate.rounds.at(-1).p2;
            const movesThatBeat = this.getMovesThatBeat(lastMove);

            if (movesThatBeat?.includes('D') && this.dynamiteCount === 0) {
                choice = this.pickRandomFrom(movesThatBeat.slice(0,movesThatBeat.length-1));
            } else {
                choice = this.pickRandomFrom(movesThatBeat);
            }
        }

        if (choice === 'D') this.dynamiteCount--;
        return choice;
    }
}

module.exports = new beatLastMoveBot();
