// class CopyLastMoveBot {

//     dynamiteCount: number;

//     constructor() { 
//         this.dynamiteCount = 100;
//     }

//     pickRandomFrom(array: string[]) {
//         return array[Math.floor(Math.random() * array.length)];
//     }

//     makeMove(gamestate: any) {

//         let choice;

//         if (gamestate.rounds.length === 0) {
//             choice = this.pickRandomFrom(['R', 'P', 'S', 'W', 'D']);
//         } else {

//             const lastMove = gamestate.rounds.at(-1).p2;
//             if (lastMove === 'D' && this.dynamiteCount === 0) {
//                 choice = this.pickRandomFrom(['R', 'P', 'S', 'W', 'D']);
//             } else {
//                 choice = lastMove;
//             }

//         }

//         if (choice === 'D') this.dynamiteCount--;
//         return choice;
//     }
// }

// module.exports = new CopyLastMoveBot();