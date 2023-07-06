const SOS_TAG = "";
const EOS_TAG = "";

function getTransitionProbs() {

}

function getEmissionProbs() {

}


/**
 * Given a set of trained transition and emission probabilities,
 * the function will predict the associated moves chosen for each
 * outcome within the provided list of of round outcomes using the
 * Viterbi Algorithm.
 * 
 * @param wordList 
 * @param tagSet 
 * @param tProbs 
 * @param eProbs 
 */
function viterbi(wordList: any, tagSet: any, tLogProbs: any, eLogProbs: any) {

    const length = wordList.length;

    // -- Build Data Structures -- //
    let v: any[] = []; // list of dict -> implement as object?
    for (let i=0; i < length+1; i++) v.push({});

    let backpointers: any[] = []; // lsit of dict -> implement as object?
    for (let i=0; i < length+1; i++) backpointers.push({});

    // -- Initialisation Step -- //
    for (const tag of tagSet) {
        v[0][tag] = tLogProbs[SOS_TAG][tag] + eLogProbs[tag][wordList[0]];
        backpointers[0][tag] = SOS_TAG;
    }

    // -- Forward Propagation Step -- //
    for (let i=1; i < length; i++) {

        for (let currTag of tagSet) {
            let probToMax = (prevTag: string) => (v[i-1][prevTag] + tLogProbs[prevTag][currTag] + eLogProbs[currTag][wordList[i]]);

            [v[i][currTag], backpointers[i][currTag]] = probAndArgMax(probToMax, tagSet);
        }

    }

    // -- Final Step -- //
    let probToMax = (prevTag: string) => (v[length-1][prevTag] + tLogProbs[prevTag][EOS_TAG]);
    [v[length][EOS_TAG], backpointers[length][EOS_TAG]] = probAndArgMax(probToMax, tagSet); 

    // -- Return Moves -- //
    return recoverMoves(backpointers);

}

function recoverMoves(backpointers: any) {

    let tagList = [];
    let currTag = EOS_TAG;

    // -- Reconstruct Moves Sequence from  Backpointers -- //
    for (let i=backpointers.length-1; i > 0; i--) {
        currTag = backpointers[i][currTag];
        tagList.push(currTag);
    }

    return tagList.reverse();

}

function probAndArgMax(probToMax: any, tagSet: any) {

    let maxProb = Number.NEGATIVE_INFINITY;
    let maxTag = null;

    for (let prevTag of tagSet) {

        let prob = probToMax(prevTag);

        if (prob > maxProb) {
            maxProb = prob;
            maxTag = prevTag;
        }

    }

    return [maxProb, maxTag];

}
