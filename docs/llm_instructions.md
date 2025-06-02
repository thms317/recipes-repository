# Recipe Reformatting Guide

## Goal

Convert raw recipe text into structured Markdown while preserving the original language and information.

## Output Format

```markdown
# Recipe Title

> *Brief description (omit dot at the end of the sentence)*

## Recipe Information

- **Prep Time:** X minutes
- **Cook Time:** X minutes
- **Rest Time:** X minutes
- **Total Time:** X minutes
- **Servings:** X servings
- **Course:** starter, main, dessert, side
- **Difficulty:** simple, medium, complex
- **Language:** EN / NL

## Ingredients

- Ingredient 1
- Ingredient 2

## Instructions

1. First step
2. Second step

## Recipe Notes

- Note 1
- Note 2
```

## Conversion Steps

1. **Title & Description**
   - Convert recipe name to H1 heading (`# Title`)
   - Format description in italics below title, led by a `>`

2. **Recipe Information**
   - Format as bulleted list with bold categories
   - Include timing, servings, and other key details from original
   - Add category and difficulty if present in original
   - If category is not present, omit

3. **Ingredients**
   - Use H2 heading (`## Ingredients`)
   - Group ingredients logically without category headers (proteins together, vegetables together, herbs together, etc.)
   - Format as single bulleted list
   - Convert all measurements to metric system (grams, milliliters, celsius)
   - Keep tablespoons (tbsp) and teaspoons (tsp) - do NOT convert to cups
   - Never include fahrenheit or imperial measurements in brackets
   - Exclude basic cooking elements like oil, salt, pepper from ingredients list

4. **Instructions**
   - Use H2 heading (`## Instructions`)
   - Only use H3 subcategories if recipe has multiple distinct phases
   - Format as numbered list
   - Preserve exact wording of each step as much as possible
   - Remove specific quantities from instructions when they're already listed in ingredients

5. **Notes**
   - Include only if present in original
   - Format as bulleted list

6. **Final Check**
   - Correct obvious spelling errors
   - Verify formatting (## for sections, ### for subsections)
   - Ensure no information was invented or omitted
   - IMPORTANT: ensure output is ready to copy and paste

## Key Principles

- Preserve original language - never translate
- Don't invent missing information
- Maintain original terminology for techniques and dishes
- Fix obvious typos but preserve technical terms
- Use proper Markdown headings (# for title, ## for sections, ### for subsections)
- Always output in artifact format for easy copying
- Metric system only - no imperial conversions in brackets
- Group ingredients logically but without category headers
