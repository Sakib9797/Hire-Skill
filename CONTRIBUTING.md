# Contributing to HireSkill

Thanks for your interest in contributing! Here's how to get started.

## Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/Hire-Skill.git
   cd Hire-Skill
   ```

2. **Backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env       # Fill in your values
   python run.py
   ```

3. **Frontend**
   ```bash
   cd frontend
   npm install
   cp .env.example .env.local
   npm start
   ```

## Code Style

- **Python**: Follow PEP 8. Use `logging` instead of `print()`.
- **JavaScript**: Follow the existing ESLint config. No `console.log` in committed code.

## Pull Requests

1. Fork the repo and create your branch from `main`.
2. Write clear commit messages.
3. If you add a feature, add a test.
4. Make sure `pytest` and `npm run build` pass.
5. Open a PR with a brief description of your changes.

## Reporting Issues

Open a GitHub Issue with:
- Steps to reproduce
- Expected vs. actual behaviour
- Screenshots if applicable

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
