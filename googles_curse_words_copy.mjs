import { ProfanityEngine } from '@coffeeandfun/google-profanity-words';
import fs from 'fs';

async function main() {
    const profanity = new ProfanityEngine({ language: 'en' });

    // const allWords = await profanity.all();
    // console.log(allWords.toString());
    
    const genres = ["pop", "rock", "country", "rap", "RB"];

    for (const genre of genres) {
        fs.promises.readFile('data/generatedJson/V5_commas/'+ genre +'LyricsFiltered_With_commas.json', 'utf8').then(async data => {
            try {
                const jsonData = JSON.parse(data);
                var curse = 0;
                var noCurse = 0;
                for (const jsonObject of Object.values(jsonData)) {
                    const lyrics = jsonObject["lyrics"].trim();
                    const hasCurseWord = await profanity.hasCurseWords(lyrics);
                    if (hasCurseWord){
                        curse += 1;                    
                    } else {
                        noCurse += 1;
                    }
                }
                const percentage = (curse / (curse + noCurse)) * 100
                console.log(genre + ": " + curse + " songs with at least 1 curse word. " + noCurse + " songs without curse words. Percentage of songs with curse word: " + percentage)
            } catch (parseError) {
                console.error('Error parsing JSON data:', parseError);
            }
        }).catch(err => {
            console.error('Error reading file:', err);
        });
    }
}

main().catch(error => {
    console.error(error);
});




// import { ProfanityEngine } from '@coffeeandfun/google-profanity-words';

// const profanity = new ProfanityEngine({ language: 'en' });

// // const allWords = await profanity.all();
// // console.log(allWords.toString());
// // console.log("\n" + allWords.length)

// const song = "hello   \n  hello"
// const hasCurseWord = await profanity.hasCurseWords(song);
// console.log(hasCurseWord)
    
