class DynamiteBot {

    dynamiteCount: number;

    constructor(){
        this.dynamiteCount = 100;
    }

    pickRandomFrom(array: string[]) {
        return array[Math.floor(Math.random() * array.length)];
    }

    makeMove(gamestate: any) {
        if (this.dynamiteCount-- > 0) {
            return 'D';
        } 

        return this.pickRandomFrom(['R', 'P', 'S', 'W']); 
    }
}

module.exports = new DynamiteBot();