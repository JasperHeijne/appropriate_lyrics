import { ProfanityEngine } from '@coffeeandfun/google-profanity-words';
import fs from 'fs';

async function main() {
    const profanity = new ProfanityEngine({ language: 'en' });

    // const allWords = await profanity.all();
    // console.log(allWords.toString());
    
    const genres = ["country", "pop", "rap", "RB", "rock"];

    for (const genre of genres) {
        fs.promises.readFile('data/generatedJson/V5_commas/'+ genre +'LyricsFiltered_With_commas.json', 'utf8').then(async data => {
            try {
                // Parse the JSON data
                const jsonData = JSON.parse(data);
                var curse = 0;
                var noCurse = 0;
                var proportions = [];
                // console.log('Data from JSON file:', jsonData);
                for (const jsonObject of Object.values(jsonData)) {
                    // console.log(jsonObject["lyrics"])
                    const lyrics = jsonObject["lyrics"];
                    // const hasCurseWord = await profanity.hasCurseWords(lyrics);
                    const words = lyrics.split(/\s+/);
                    for (const word of words){
                        if (await profanity.search(word)) {
                            curse += 1;
                        } else {
                            noCurse += 1;
                        }
                    }
                    const proportion = curse/(curse + noCurse);
                    proportions.push(proportion);
                    // console.log(genre + " has curse words/totalwords: " + proportion)
                }
                fs.writeFile('data/results_curse_words_proportions/' + genre + "Proportions", proportions.join('\n'), (err) => {
                    if (err) {
                      console.error('Error writing to file:', err);
                      return;
                    }
                    console.log(genre + ' data written to file successfully!');
                  });
                // var averageProportion = 0;
                // for (const prop of proportions){
                //     averageProportion += prop;
                // }
                // averageProportion = averageProportion / proportions.length
                // console.log(genre + ": " + averageProportion);
                // console.log(genre + ": " + curse + " songs with at least 1 curse word. " + noCurse + " songs without curse words.")
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