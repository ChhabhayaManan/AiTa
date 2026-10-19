export const TOPIC_LABELS = {
  basics_io: 'Basics & I/O',
  conditionals: 'Conditionals',
  loops: 'Loops',
  functions: 'Functions',
  arrays: 'Arrays',
  strings: 'Strings',
  hashing_sets: 'Hashing & Sets',
  recursion: 'Recursion',
  sorting: 'Sorting',
  searching: 'Searching',
  stacks_queues: 'Stacks & Queues',
  dynamic_programming: 'Dynamic Programming',
}

export const MISCONCEPTION_LABELS = {
  off_by_one: 'Off by one',
  empty_input_unhandled: 'Empty input not handled',
  wrong_initial_value: 'Wrong starting value',
  wrong_comparison_operator: 'Wrong comparison (< vs <=)',
  integer_division: 'Integer vs true division',
  missing_base_case: 'Missing base case',
  mutate_while_iterating: 'Changing a list while looping over it',
  uninitialised_variable: 'Variable not reset / initialised',
  wrong_loop_bound: 'Wrong loop bound',
  return_vs_print: 'Return vs print',
  index_out_of_range: 'Index out of range',
  infinite_loop: 'Loop never ends',
}

export const BAND_STYLE = {
  unseen:     { label: 'Not yet practised', bar: 'bg-white/10',   text: 'text-white/30' },
  weak:       { label: 'Weak',              bar: 'bg-red-500',    text: 'text-red-400' },
  developing: { label: 'Developing',        bar: 'bg-yellow-500', text: 'text-yellow-400' },
  mastered:   { label: 'Mastered',          bar: 'bg-green-500',  text: 'text-green-400' },
}

export const ITEM_TYPE_LABELS = {
  diagnostic: 'Diagnostic',
  mcq: 'Multiple choice',
  coding: 'Coding problem',
  debug: 'Debug challenge',
}

export const EVENT_KIND_LABELS = {
  code: 'Coding',
  mcq: 'MCQ',
  diagnostic: 'Diagnostic',
  debug: 'Debug',
  diagnostic_seed: 'Starting check',
  diagnostic_theory: 'Starting check (theory)',
}

export const topicLabel = t => TOPIC_LABELS[t] || t || 'Unclassified'
export const misconceptionLabel = m => MISCONCEPTION_LABELS[m] || m
