class WDCountingBot {

    dynamiteCount: number;
    enemyDynamiteCount: number;
    availableMoves: string[];

    constructor() {
        this.dynamiteCount = 100;
        this.enemyDynamiteCount = 100;
        this.availableMoves = ['R', 'P', 'S', 'W', 'D'];
    }

    pickRandomFrom(array: string[]) {
        return array[Math.floor(Math.random() * array.length)];
    }

    doInitialMove() {
        const move = this.pickRandomFrom(this.availableMoves);

        if (move === 'D') this.dynamiteCount--;
        return move;
    }

    makeMove(gamestate: any) {

        if (gamestate.rounds.length === 0) {
            return this.doInitialMove();
        }

        const enemylastMove = gamestate.rounds.at(-1).p2;

        if (enemylastMove === 'D') this.enemyDynamiteCount--;

        if (this.enemyDynamiteCount === 0) {
            this.availableMoves = this.availableMoves.filter((value) => value !== 'W');
        }

        if (this.dynamiteCount === 0) {
            this.availableMoves = this.availableMoves.filter((value) => value !== 'D');
        }

        const choice = this.pickRandomFrom(this.availableMoves);
        if (choice === 'D') this.dynamiteCount--;

        return choice;
    }
}

module.exports = new WDCountingBot();