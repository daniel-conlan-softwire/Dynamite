

// class RandomBot {

//     dynamiteCount: number;

//     constructor() {
//         this.dynamiteCount = 100;
//     }

//     pickRandomFrom(array: string[]) {
//         return array[Math.floor(Math.random() * array.length)];
//     }

//     makeMove(gamestate: any) {

//         if (this.dynamiteCount > 0) {
//             const choice = this.pickRandomFrom(['R', 'P', 'S', 'W', 'D']);
//             if (choice === 'D') this.dynamiteCount--;
            

//             return choice;
//         } else {
//             return this.pickRandomFrom(['R', 'P', 'S']);
//         }


//     }
// }

// module.exports = new RandomBot();