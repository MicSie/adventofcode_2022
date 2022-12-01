def part1(calories: list) -> int:
  return max(calories)

def part2(calories: list) -> int:
  return sum(sorted(calories, reverse=True)[:3])

def read_calories_from_file(fileName: str) -> list:
  lines = read_file(fileName)
  return sum_lines(lines)

def read_file(fileName: str) -> list:
  with open(fileName, 'r') as file:
    return [line.strip() for line in file]

def sum_lines(lines: list) -> list:
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
  calories = read_calories_from_file('input')
  print('Part1: '+str(part1(calories)))
  print('Part2: '+str(part2(calories)))