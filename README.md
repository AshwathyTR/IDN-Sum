# IDN-Sum
Dataset for Interactive Narrative Summarisation

This repository contains code used to generate data in IDN-Sum.  

Use bts_readerbot branch to generate playthroughs of Before the Storm and wau_readerbot branch to generate playthroughs for Wolf Among Us.

## Usage:  
To run the readerbot :  

    python main.py <number_of_playthroughs> <output_folder>  

To split up episodes :  

    python split_episodes.py  <path_to_generated_playthroughs>

To clean data and add [EX] and S0 markers :  

    python clean_script.py <input_path> <number_of_playthroughs>  

To prep data in format similar to CNN/DailyMail :  

    python prep_data.py <path_to_generated_playthroughs> <path_to_abstractive_summary> <file_name>

Annotations for extractive summarisation was generated using conversion script from TransformerSum [1]. 
Alternatively, data in all formats may be downloaded from [link to be added].

## Implementation

To ensure that the ReaderBot generates a wide variety of playthroughs through the game, it keeps track of all the choice combinations it has generated previously. In each step, it makes the choice that creates a choice combination that has minimum overlap with the combinations generated so far. The choices taken for each playthrough are provided along with the simulated playthrough. Note that the ReaderBot simulates playthroughs through the game capturing major aspects of the game, but it does not perfectly mimic it (for example, not all game mechanics in the game are reflected in the ReaderBot).

## Support for game mechanics:  

The following game mechanics are supported: 
   
	1. Choices and consequences in both games (ref set_triggers.json and use_triggers.json)  
	2. Counters to keep track of variables like romance score in Before the Storm (ref counters.json)  
	3. Backtalk in Before the Storm ( ref backtalk_scores.json and bt_triggers.json)  
	4. Flags for scenes (ref scene_triggers.json)  
	5. Order of scenes in Wolf Among Us  
	6. Optional interactions in Wolf Among Us where player can make multiple choices.  
	
## Limitations:  

The readerbot simulates playthroughs but doesn't perfectly mimic the game. 

	1. Order is only accounted for major scenes in Wolf Among Us.  
	2. Assumption is that you can chose only one option at a choice point except in Wolf Among Us where it is explicitly under a heading that says "Optional interactions".  
	3. Minor in game game mechanics excluded - eg. two truths and a lie in Before the Storm.  
	4. Assumptions were made where details of implementation not clear from script text. Set and use triggers are not thorough (all connections important to story are included and all consequences in brackets were reviewed but minor dialogue changes may be missed out esp if connection is described in text and not in title).  
	5. Wolf among us script is incomplete - some sections are TBC and set triggers could not be found for some use triggers.  
	6. Order is accounted for only in case of major consequences (going to which scene first in Wolf Among Us), not for optional interactions.  
	7. Sometimes "examine x" is in the text and not as an option, but there are use triggers before/after this which will always be set to examined or didn't examine depending on where in the script the text is.  


## Models:
Models were trained using scripts from TransformerSum[1] and Summarunner[2]. Summarunner-long was trained using small modifications to the original Summarunner script, allowing it to accept a maximum document length. A fork of Summarunner with this modification can be found at <link to be added>.
Models can be downloaded from [link to be added].

## Results:
Predictions were made using scripts from TransformerSum and SumaRuNNer. ROUGE scores were calculated using eval script from SummaRuNNer. Output from these models can be found at [link to be added]. Results are shown below along with rand-n (random n sentences), lead-n (first n sentences) and textrank (from gensim[3]) baselines for reference:
[Table with results to be added]

## References:
[1]https://github.com/HHousen/TransformerSum <br />
[2]https://github.com/hpzhao/SummaRuNNer <br />
[3]https://radimrehurek.com/gensim_3.8.3/auto_examples/tutorials/run_summarization.html
