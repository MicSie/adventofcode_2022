def Part1(calories: list) -> int:
  return max(calories)

def Part2(calories: list) -> int:
  return sum(sorted(calories, reverse=True)[:3])

def ReadCaloriesFromFile(fileName: str) -> list:
  lines = ReadFile(fileName)
  return SumLines(lines)

def ReadFile(fileName: str) -> list:
  with open(fileName, 'r') as file:
    return [line.strip() for line in file]

def SumLines(lines: list) -> list:
  result = []
  current = 0
  for line in lines:
    if(len(line) == 0):
      if(current > 0):
        result.append(current)
        current = 0
    else:
      current += int(line)

  if(current > 0):
    result.append(current)
  return result

if __name__ == '__main__':
  calories = ReadCaloriesFromFile('input')
  print('Part1: '+str(Part1(calories)))
  print('Part2: '+str(Part2(calories)))