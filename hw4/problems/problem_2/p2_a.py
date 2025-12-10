# Problem 2 a 

def linear_search(packages, boxes):

    least_waste = float('inf')
    possible = False

    for supplier in boxes:
        cur_waste = 0
        can_use = True

        for package_size in packages:
            best_fit = None

            for box_size in supplier:
                if box_size >= package_size:
                    if best_fit is None or box_size < best_fit:
                        best_fit = box_size

            if best_fit is None:
                can_use = False
                break

            cur_waste += best_fit - package_size

        if can_use:
            possible = True
            least_waste = min(least_waste, cur_waste)

    return least_waste if possible else -1
