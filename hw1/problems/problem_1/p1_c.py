'''
Problem 1c

input: File containing an integer n followed by 2n lines containing the preferences of the n students and then the n hospitals (see README).
output: Dictionary mapping students to hospitals. 

TODO: Implement the Gale-Shapley algorithm to run in O(n^2).
'''
def stable_matching_1c(file) -> dict:
    n = 0
    doctors_pref = []
    hospitals_pref = []

    with open(file, "r") as f:
        n = int(f.readline())
        for _ in range(n):
            d_pref = f.readline().split()
            doctors_pref.append([int(x) for x in d_pref])

        for _ in range(n):
            h_pref = f.readline().split()
            hospitals_pref.append([int(x) for x in h_pref])

    # doctors to hospitals map
    pairs = {}

    # set of hospitals with no doctor
    doctorless_hospitals = set()
    for i in range(n):
        doctorless_hospitals.add(i)

    # i = hospital i
    # arr[i] = best rank that this hospital is able to attempt to match
    best_rank_for_hospital = [0] * n

    # hospital_rankings[i] = doctor i's ranking of hospitals
    # hospital_rankings[i][j] = doctor i's ranking for hospital j
    hospital_rankings_for_doctor = []
    for hospitals in doctors_pref:
        hospital_ranking_for_this_doc = [0] * n
        rank = 0
        for hospital in hospitals:
            hospital_ranking_for_this_doc[hospital] = rank
            rank += 1
        hospital_rankings_for_doctor.append(hospital_ranking_for_this_doc)

    while len(doctorless_hospitals) > 0:
        doctorless_hospital = doctorless_hospitals.pop()
        best_rank = best_rank_for_hospital[doctorless_hospital]

        # This hospital's preferred doctor at the moment
        pref_doc = hospitals_pref[doctorless_hospital][best_rank]

        # Doctor doesn't have a match, match with this hospital
        current = pairs.get(pref_doc, -1)
        if current == -1:
            pairs[pref_doc] = doctorless_hospital
        else:
            # Doctor switches for this hospital since it prefers this new one
            if hospital_rankings_for_doctor[pref_doc][doctorless_hospital] < hospital_rankings_for_doctor[pref_doc][current]:
                doctorless_hospitals.add(current)
                pairs[pref_doc] = doctorless_hospital
            else:
                doctorless_hospitals.add(doctorless_hospital)

        # Update rank in case next doctor needs to be considered
        best_rank_for_hospital[doctorless_hospital] += 1

    return pairs
