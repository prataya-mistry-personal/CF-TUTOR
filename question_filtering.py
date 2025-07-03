#!/usr/bin/env python3
"""
Codeforces Tutor - Question Filtering Module
Filters Codeforces problems based on user criteria
"""
from email.policy import default

import requests
import json
import sys
from typing import List, Dict, Any

def get_user_input_int(prompt: str, min_val: int = 800, max_val: int = 3500, default: int = None) -> int:
    """Get integer input from user with validation"""
    while True:
        try:
            user_input = input(prompt).strip()
            if user_input == "":
                return default
            value = int(user_input)
            if min_val is not None and value < min_val:
                print(f"Value must be at least {min_val}")
                continue
            if max_val is not None and value > max_val:
                print(f"Value must be at most {max_val}")
                continue
            return value
        except ValueError:
            print("Please enter a valid integer.")
        except KeyboardInterrupt:
            print("\nReturning to main menu...")
            return None

def get_rating_range():
    """Get rating range from user"""
    print("\n--- Rating Range ---")
    print("Enter 800 for no lower bound, 3500 for no upper bound")

    lower_bound = get_user_input_int("Rating range lower bound (type 800 for no lower_bound): ", min_val=800, max_val=3500,default = 800)
    upper_bound = get_user_input_int("Rating range upper bound (type 3500 for no upper_bound): ", min_val=lower_bound, max_val=3500, default = 3500)
    return lower_bound, upper_bound

def get_contest_type():
    """Get contest type preference from user"""
    print("\n--- Contest Type Preference ---")
    print("1. Educational")
    print("2. Normal Div 2")
    print("3. Div 1+2")
    print("4. Div 3")
    print("5. Div 4")
    print("6. No preference")

    choice = get_user_input_int("Contest type preference (1-6): ", min_val=1, max_val=6, default = 6)
    if choice is None:
        return None

    contest_types = {
        1: "educational",
        2: "div2",
        3: "div12",
        4: "div3",
        5: "div4",
        6: "no_preference"
    }

    return contest_types[choice]

def get_question_range():
    """Get question number preference from user"""
    print("\n--- Question Number Preference ---")
    print("Example: write '2 5' for considering questions 2 to 5 (1-indexed) or write 4 for only question number 4")
    print("Type '0' for no preference")

    while True:
        try:
            user_input = list(map(int, input("Enter list elements: ").split()))
            if len(user_input) == 0 or (len(user_input) == 1 and user_input[0] == 0):
                return 1, 10
            if len(user_input) == 1:
                return user_input[0], user_input[0]

            if len(user_input) == 2:
                if 1 <= user_input[0] <= user_input[1] <= 10:
                    return user_input[0], user_input[1]
                else:
                    print("Question numbers must be between 1-10 and start <= end")
            else:
                print("Please enter two numbers separated by space, or single integer, or '0' for no preference")
        except ValueError:
            print("Please enter valid integers")
        except KeyboardInterrupt:
            print("\nReturning to main menu...")
            return None, None

def get_contest_count():
    """Get number of recent contests to consider"""
    print("\n--- Recent Contests ---")
    count = get_user_input_int("Last how many contests to be considered (1-500): ", min_val=1, max_val=500, default=500)
    return count

def get_max_questions():
    """Get maximum number of questions wanted"""
    print("\n--- Maximum Questions ---")
    max_q = get_user_input_int("Maximum number of questions you want: ", min_val=1, max_val=1000, default=10)
    return max_q

def fetch_problems_and_contests():
    """Fetch problems and contests from Codeforces API"""
    try:
        print("\nFetching problems from Codeforces API...")

        # Fetch problems
        problems_url = "https://codeforces.com/api/problemset.problems"
        problems_response = requests.get(problems_url, timeout=10)

        if problems_response.status_code != 200:
            print(f"Error fetching problems: HTTP {problems_response.status_code}")
            return None, None

        problems_data = problems_response.json()
        if problems_data['status'] != 'OK':
            print(f"API Error: {problems_data.get('comment', 'Unknown error')}")
            return None, None

        # Fetch contests
        print("Fetching contests from Codeforces API...")
        contests_url = "https://codeforces.com/api/contest.list"
        contests_response = requests.get(contests_url, timeout=10)

        if contests_response.status_code != 200:
            print(f"Error fetching contests: HTTP {contests_response.status_code}")
            return problems_data['result'], None

        contests_data = contests_response.json()
        if contests_data['status'] != 'OK':
            print(f"Contest API Error: {contests_data.get('comment', 'Unknown error')}")
            return problems_data['result'], None

        return problems_data['result'], contests_data['result']

    except requests.exceptions.Timeout:
        print("Request timeout. Please check your internet connection.")
        return None, None
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        return None, None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None, None

def classify_contest_type(contest_name: str) -> str:
    """Classify contest type based on name"""
    name_lower = contest_name.lower()

    if 'educational' in name_lower:
        return 'educational'
    elif 'div. 1' in name_lower and 'div. 2' in name_lower:
        return 'div12'
    elif 'div. 2' in name_lower:
        return 'div2'
    elif 'div. 3' in name_lower:
        return 'div3'
    elif 'div. 4' in name_lower:
        return 'div4'
    else:
        return 'other'

def filter_problems(problems: List[Dict], contests: List[Dict], filters: Dict) -> List[Dict]:
    """Filter problems based on user criteria"""

    # Create contest lookup
    contest_lookup = {c['id']: c for c in contests} if contests else {}

    filtered = []

    for problem in problems:
        # Skip gym problems (contestId >= 100000)
        if problem['contestId'] >= 100000:
            continue

        # Rating filter
        if 'rating' in problem:
            rating = problem['rating']
            if filters['rating_lower'] is not None and rating < filters['rating_lower']:
                continue
            if filters['rating_upper'] is not None and rating > filters['rating_upper']:
                continue
        elif filters['rating_lower'] is not None or filters['rating_upper'] is not None:
            # Skip problems without rating if rating filter is specified
            continue
        else:
            continue

        # Contest type filter
        if filters['contest_type'] != 'no_preference' and contests:
            contest_id = problem['contestId']
            if contest_id in contest_lookup:
                contest = contest_lookup[contest_id]
                contest_type = classify_contest_type(contest['name'])
                if contest_type != filters['contest_type']:
                    continue

        # Question number filter (problem index)
        if filters['question_start'] is not None and filters['question_end'] is not None:
            index = problem['index']
            # Convert index to number (A=1, B=2, etc.)
            if len(index) >= 1 and index[0].isalpha():
                index_num = ord(index[0].upper()) - ord('A') + 1
                if index_num < filters['question_start'] or index_num > filters['question_end']:
                    continue

        filtered.append(problem)

    # Recent contests filter
    if filters['contest_count'] and contests:
        # Get recent contest IDs
        recent_contests = sorted(contests, key=lambda c: c.get('startTimeSeconds', 0), reverse=True)
        recent_contest_ids = set()
        finished_count = 0

        for contest in recent_contests:
            if contest['phase'] == 'FINISHED':
                recent_contest_ids.add(contest['id'])
                finished_count += 1
                if finished_count >= filters['contest_count']:
                    break

        # Filter problems to only recent contests
        filtered = [p for p in filtered if p['contestId'] in recent_contest_ids]

    # Limit number of results
    if filters['max_questions']:
        filtered = filtered[:filters['max_questions']]

    return filtered

def display_results(problems: List[Dict]):
    """Display filtered problems as links"""
    if not problems:
        print("\nNo problems found matching your criteria.")
        return

    print(f"\nFound {len(problems)} problems matching your criteria:")
    print("-" * 60)

    for problem in problems:
        contest_id = problem['contestId']
        index = problem['index']
        link = f"https://codeforces.com/problemset/problem/{contest_id}/{index}"
        print(link)

def filter_questions(username: str):
    """Main question filtering function"""
    print(f"\n=== QUESTION FILTERING FOR USER: {username} ===")

    # Get user preferences
    rating_lower, rating_upper = get_rating_range()
    if rating_lower is None or rating_upper is None:
        return

    contest_type = get_contest_type()
    if contest_type is None:
        return

    question_start, question_end = get_question_range()
    if question_start is None and question_end is None:
        return

    contest_count = get_contest_count()
    if contest_count is None:
        return

    max_questions = get_max_questions()
    if max_questions is None:
        return

    # Create filters dictionary
    filters = {
        'rating_lower': rating_lower,
        'rating_upper': rating_upper,
        'contest_type': contest_type,
        'question_start': question_start,
        'question_end': question_end,
        'contest_count': contest_count,
        'max_questions': max_questions
    }

    # Fetch data and filter
    problems_data, contests_data = fetch_problems_and_contests()
    if problems_data is None:
        print("Failed to fetch data from Codeforces API.")
        return

    problems = problems_data['problems']
    contests = contests_data if contests_data else []

    print(f"\nFiltering {len(problems)} problems...")
    filtered_problems = filter_problems(problems, contests, filters)

    # Display results
    display_results(filtered_problems)

    print(f"\nFiltering complete!")
    input("\nPress Enter to return to main menu...")

if __name__ == "__main__":
    # Test the module
    filter_questions("test_user")
