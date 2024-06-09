# Confiabilidade de Sistemas Distribuídos 2023-24

# Project 2 | Option 2 | Francisco Vasco 61028 & Tomé Dias 60719
 
## Setup
To setup the project libraries run:

```
sh setup.sh
```

## Linkage Attack
Run the linkage attack:
```
python linkage_atk.py {marriage_file} {earnings_file} {sti_file}
```


## K-Anonimity
Run the generalizer and the k-anonymity tester, respectively:
```
python generalizer.py {input_file} {k-value}

python k-anon.py {generalized_file} {k-value}
```
### k=2
The dataset was not 2-anonymous, and
we needed to run the generalization program.

After running the program for k=2 the dataset was 2-anonymous.

Our generalization was as follows:

"Education Status" in range [1,9]->1 and [10-16]->2
Months for "Date of Birth" in range [1,6]->1 and [7,12]->2

Days for "Date of Birth" in range [1,10]->10, [11,20]->20 and [21-31]->30

"Postal Code" -> XXXX

Utility: we lost all the utility of the postal code information but we were able to perserve  some information about the individuals' birthdays as well as their education and education status.

### k=3
The dataset was not 3-anonymous, and
we needed to run the generalization program.

After running the program for k=3 the dataset was 3-anonymous.

Our generalization was as follows:

"Education Status" in range [1,9]->1, [10-12]->2 and [13,16]->3

Years for "Date of Birth" were rounded down to the closest multiple of 50

Months for "Date of Birth" in range [1,3]->1, [4,6]->2, [7,9]->3 and [10,12]->4

Days for "Date of Birth" in range [1,15]->15 and [16,31]->30

"Postal Codes" were truncated e.g. 1234->12XX

Utility: we lost a lot of utility on the information about dates of birth but we now have some information on the general region of the individuals.

### k=4 and k=5
The dataset was not 4-anonymous, and
we needed to run the generalization program.

After running the program for k=4 the dataset was 4-anonymous.

We were not able to achieve a generalization that worked solely for k=4, so it generalizes for both k=4 (and of course all k<4) and k=5.

Our generalization was as follows:

Same generalizations as k=3 for "Education Status",year and "Postal Code"

Months for "Date of Birth" in range [1,2]->1, [3,4]->2, [5,6]->3, [7,8]->4, [9,10]->5, [11,12]->6

Days for "Date of Birth" -> "00"

Utility: we lost even more utility when it comes to the dates of birth than we did for k=3 because, even though we have more information when it comes to each month, we now have no information about the days of birth.

## Differential Privacy
Run the Differential Privacy query system:
```
python differential_privacy.py {data_file}
```