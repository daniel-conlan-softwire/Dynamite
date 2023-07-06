// import { dynamiteBot } from "../basicBots/dynamiteBot";
// import { randomBot } from "../basicBots/randomBot";
// import { beatLastMoveBot } from "../copyBasedBots/beatLastMoveBot";

// class Bots {} // all other bots should extend from this (can also be an interface)

// class Statistics{

//     getData(gamestate: any){

//         let enemyDynamiteCount: number = 0;
//         let enemyConsecutiveWaterCount: number = 0;
//         let enemyConsecutiveDynamiteCount: number = 0;
//         let wonAgainstRockCount: number = 0;
//         let wonAgainstPaperCount:number = 0;
//         let wonAgainstScissorsCount: number = 0;
//         let wonAgainstDynamiteCount: number = 0;
//         let wonAgainstWaterCount: number = 0;
//         let lostAgainstRockCount: number = 0;
//         let lostAgainstPaperCount:number = 0;
//         let lostAgainstScissorsCount: number = 0;
//         let lostAgainstDynamiteCount: number = 0;
//         let lostAgainstWaterCount: number = 0;

//         for (const thisRound of gamestate.rounds){
//             const p1Move = thisRound.p1;
//             const p2Move = thisRound.p2;
//             if (p2Move === 'R') {
//                 if (['P', 'D'].includes(p1Move)) {
//                     wonAgainstRockCount++;
//                 } else {
//                     lostAgainstRockCount++;
//                 }
//             } else if (p2Move === 'P') {
//                 if (['S','D'].includes(p1Move)) {
//                     wonAgainstPaperCount++;
//                 } else {
//                     lostAgainstPaperCount++;
//                 }
//             } else if (p2Move === 'S') {
//                 if (['R','D'].includes(p1Move)) {
//                     wonAgainstScissorsCount++;
//                 } else {
//                     lostAgainstScissorsCount++;
//                 }
//             } else if (p2Move === 'D') {
//                 if (['W'].includes(p1Move)) {
//                     wonAgainstDynamiteCount++;
//                 } else {
//                     lostAgainstDynamiteCount++;
//                 }
//             } else if (p2Move === 'W') {
//                 if (['R','P','S'].includes(p1Move)) {
//                     wonAgainstWaterCount++;
//                 } else {
//                     lostAgainstWaterCount++;
//                 }
//             }
//         }        

//     }
// }

// class dynamicBot {

//     allStrategyBots: Bots[]
//     gameStatistics: Statistics;

//     constructor () {
//         this.allStrategyBots = []; 
//     }

// }