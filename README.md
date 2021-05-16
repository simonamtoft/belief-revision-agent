# Belief Revision Agent
A belief revision engine made for the Intro to AI course on DTU.


## Install required packages
Run the following in the root directory: 

```pip install -r requirements.txt```


## Running the Program
To run the program, simply navigate to the project folder, ensure you have python installed, and the required packages.

Then run one of the following:

```python
# cli program
python program.py

# programs to test AGM postulates
python test_agm_contraction.py
python test_agm_revision.py
```


## Program Syntax
The cli program follows the below syntax for logical input expression

| Logic | Program Input |
| ----- | ----- |
| a OR b | a \| b | 
| a AND b | a & b | 
| NOT a | ~a| 
| a IMPLIES b | a >> b|
| a BI-IMPLICATION b | a >> b & a << b |



## Collaborators

[Simon Amtoft Pedersen](https://github.com/simonamtoft/)

[Marc Sun Bøg](https://github.com/MarcMarabou)

[Janus Johansen](https://github.com/YoungPenguin)

[Eva Hvalkofff](https://github.com/Evahval)
