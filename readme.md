# Codeforces Tutor

A simple, interactive terminal-based Python application that helps users practice and analyze Codeforces problems. The tool provides two main features: intelligent problem filtering and comprehensive user analytics.

## Features

### 🔍 Question Filtering
- Filter problems by rating range (800-3500)
- Filter by contest type (Educational, Div 1, Div 2, Div 3, Div 4, Div 1+2)
- Filter by question position (A, B, C, etc.)
- Consider only recent contests
- Limit number of results
- Excludes gym problems automatically

### 📊 User Analytics
- Basic user information and ratings
- Submission statistics and acceptance rates
- Programming language usage
- Problem-solving distribution by tags
- Difficulty level analysis (rating distribution)
- Recent submission activity
- Contest performance and rating changes

## File Structure

```
codeforces_tutor/
├── main.py                # Main application entry point
├── question_filtering.py  # Problem filtering functionality
├── user_analytics.py      # User analytics functionality
└── README.md              # This file
```

## Installation

### Prerequisites
- Python 3.6 or higher
- Internet connection (for API calls)

### Dependencies
Install the required Python package:

```bash
pip install requests
```

That's it! The application only requires the `requests` library for making HTTP calls to the Codeforces API.

## Usage

### Running the Application

1. **Navigate to the project directory:**
   ```bash
   cd codeforces_tutor
   ```

2. **Run the main application:**
   ```bash
   python main.py
   ```
   or
   ```bash
   python3 main.py
   ```

3. **Follow the interactive prompts:**
   - Enter your Codeforces username when prompted
   - Choose from the main menu options
   - Follow the step-by-step instructions for filtering or analytics

### Menu Options

When you run the application, you'll see:

```
==================================================
    CODEFORCES TUTOR - MAIN MENU
==================================================
1. Question Filtering
2. User Analytics
3. fetch a new user
4. Exit
==================================================
```

## Question Filtering Guide

### Step-by-Step Process

1. **Rating Range:**
   - Enter `800` for no lower bound
   - Enter `3500` for no upper bound
   - Example: `800` to `1200` for beginner problems

2. **Contest Type:**
   - `1` for Educational rounds
   - `2` for Normal Div 2 rounds
   - `3` for Div 1+2 rounds
   - `4` for Div 3 rounds
   - `5` for Div 4 rounds
   - `6` for no preference

3. **Question Position:**
   - Enter `2 5` to consider problems B through E
   - Enter `0` for no preference
   - Enter `4` to consider problem D
   - Uses 1-indexed numbering (A=1, B=2, etc.)

4. **Recent Contests:**
   - Enter number of recent contests to consider (1-500)
   - Example: `50` for last 50 contests

5. **Maximum Results:**
   - Enter maximum number of problem links you want
   - Example: `20` for 20 problems

### Example Output

```
Found 15 problems matching your criteria:
------------------------------------------------------------
https://codeforces.com/problemset/problem/1825/A
https://codeforces.com/problemset/problem/1825/B
https://codeforces.com/problemset/problem/1824/A
...
```

## User Analytics Guide

The analytics feature provides comprehensive insights into a user's Codeforces performance:

### Information Displayed

1. **User Profile:**
   - Name, country, organization
   - Current and maximum rating
   - Rank information
   - Registration date and last activity

2. **Submission Statistics:**
   - Total submissions and acceptance rate
   - Verdict breakdown (AC, WA, TLE, etc.)
   - Unique problems attempted vs solved

3. **Programming Languages:**
   - Most used languages with percentages
   - Distribution across all submissions

4. **Problem Categories:**
   - Top 15 problem tags you've solved
   - Shows your strengths and areas of focus

5. **Difficulty Analysis:**
   - Rating distribution of solved problems
   - Helps identify skill progression

6. **Recent Activity:**
   - Last 10 submissions with verdicts
   - Problem names and timestamps

7. **Contest Performance:**
   - Rating changes over recent contests
   - Positive vs negative performance ratio

### Example Output

```
==================================================
                USER INFORMATION
==================================================
Handle: your_username
Name: John Doe
Country: United States
Current Rating: 1547
Max Rating: 1650
Rank: expert
...

==================================================
           SOLVED PROBLEMS BY TAG
==================================================
Top problem categories you've solved:
implementation: 45 problems
math: 32 problems
greedy: 28 problems
...
```

## API Information

This application uses the official Codeforces API:
- **Base URL:** `https://codeforces.com/api/`
- **Rate Limit:** 5 requests per second (handled automatically)
- **No authentication required** for the features used

### API Endpoints Used

- `problemset.problems` - Get all problems
- `contest.list` - Get contest information
- `user.info` - Get user basic information
- `user.status` - Get user submissions
- `user.rating` - Get user rating history

## Error Handling

The application handles various error scenarios:
- **Network issues:** Timeout and connection errors
- **Invalid usernames:** User not found errors
- **API limits:** Rate limiting and server errors
- **Input validation:** Invalid user inputs

## Tips for Best Results

### For Question Filtering:
- Start with a broad rating range, then narrow down
- Use recent contests filter for current meta problems
- Educational rounds are great for learning new concepts
- Div 3 and Div 4 are ideal for beginners

### For User Analytics:
- Make sure your Codeforces profile is public
- Use your exact handle (case-sensitive)
- Analytics work best with users who have submissions
- Recent activity helps track improvement

## Troubleshooting

### Common Issues:

1. **"User not found" error:**
   - Check spelling of username
   - Ensure username exists on Codeforces
   - Username is case-sensitive

2. **Network timeout:**
   - Check internet connection
   - Codeforces API might be temporarily down
   - Try again after a few minutes

3. **No problems found:**
   - Your filters might be too restrictive
   - Try broadening the rating range
   - Use "no preference" for some filters

4. **Import errors:**
   - Ensure `requests` is installed: `pip install requests`
   - Check Python version (3.6+ required)

## Contributing

This is a simple educational tool. Feel free to:
- Add more filtering options
- Fix the issue with question index selection: for 3 to 5 , question C to question E are considered but there will be problem when index of C1,C2,D1 etc exists.
- Enhance error handling
- Improve the user interface
- Add frontend integration for better user experience
- Add data visualization features
- ML integration for problem suggestion

## License

This project is open source and available under the MIT License.

## Disclaimer

This tool is not affiliated with Codeforces. It uses the public Codeforces API and respects their usage guidelines.

---

**Happy coding! 🚀**

*For questions or issues, please check the troubleshooting section or refer to the Codeforces API documentation.*
