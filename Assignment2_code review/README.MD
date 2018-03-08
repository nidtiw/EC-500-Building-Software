*** Error handling part is done as a part of the code in the form of 3 tests at the end of the code. It is consolidated in one code ***

# Following is the report containing the code review.

## Coding Style:
1. The coding style is clear and following coding standards. 
2. There are various specifications for mac and windows user which is very convenient so the user does not have to figure them out for themselves. That's great foresight on the part of the developer.

## Major Issue:
1. It is a little troubling implementing the code as there are too many arguments required to be entered on the terminal. 
2. I assess that it was done to give the user flexibility to customise the final video they will be using, but there needs to be a tradeoff. 
3. Too much flexibility will make it complicated for the user to understand and they will have to assiduously go through your code to interpret what information they are required to provide. 
4. A little less flexibility is recommended. The objective is to build an API that is user-friendly. Too many sys.argv's create undesirable confusions.

## Styling Issues: 
1. The commenting style was clear and and detailed. However, since there is a lot of command line arguments required, it should have been detailed in greater clarity in the readme document. 
2. The code should have been run through pylint to take care of indentation issues.

## Accomplishment
1. The developer has looked out for all kinds of errors which is amazing. I couldn't find any area which the developer has not accounted for.
2. Even each argument error has been documented and errors specific for windows and amc users have also been dealt with.

## One user-dependent drawback:
1. The developer has used python 2.7 syntax. It may be a personal quirk on my part, but I needed to go and change all the print statements before executing the code.
2. Even then there were many indentation issues I had to take care of. I suggest that pylint be used in order to take care of these issues.
3. This will enable it to execute seamlessly across all platforms. 
4. I want to reiterate the over-customization of the code will lead to greater confusion. An API requiring changes based on the platform it operates on is not an efficient API. It should execute seamlessly, regardless of the platform it is operating on.


