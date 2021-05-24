

# Start

# Create payoff table (lexmax f_k(X), k=1..p)

# Calculate ranges r_k for k = 2..p


# Divide r_k into g_k intervals (set number of gridpoints = g_k + 1)


# Initialize counters: i_k = 0 for k = 2...p, n_p = 0

# While i_p < g_p / or entered

    # i_p = i_p + 1

    # While i_p-1 < g_p-1 / or entered

        # i_p-1 = i_p-1 + 1

        # While i_2 < g_2 / or entered

            # i_2 = i_2 + 1

            # Solve problem P

            # If feasible

                # Then

                    # n_p = p_p + 1

                    # Calculate b, b = int(S_2/step_2)

                    # i_2 = i_2 +b

                # Else

                    # i_2 = g_2

