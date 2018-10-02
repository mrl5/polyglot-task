#!/usr/bin/env ruby

# stores path of this script
script_path = File.dirname(File.expand_path $0)
api_name = "worker.py"
# global variable: path to API
$api = File.join(script_path, api_name)

puts "Reverse Polish notation app"
puts ""
puts "Input syntax:"
puts "\tNumber of RPN expressions"
puts "\t1st RPN expression"
puts "\t2nd RPN expression"
puts "\t..."
puts "\tNth RPN expression"
puts ""
puts "If you change your mind, hit Ctrl+C to end this app"
puts ""
puts "Input:"

# save input and (.chomp) remove carriage return from end of the input string
inp = gets.chomp
# convert input to integer, if inp is a string result will be 0
no_of_expressions = inp.to_i

def get_RPN_expressions(no_of_exp)
	expressions = Array.new
	no_of_exp.times do
		expression = gets.chomp
		expressions.push(expression)
	end
	return expressions
end

def pass_to_api(arguments)
	for argument in arguments
		system( $api + " " + "\"" + argument + "\"" )
	end
end

# main
if no_of_expressions.is_a? Integer
	if no_of_expressions > 0
		expressions = get_RPN_expressions(no_of_expressions)
		puts ""
		puts "Output:"
		pass_to_api(expressions)
	else
		raise("Number of RPN expressions must be greather than 0")
	end
else
	raise("First line must be an integer")
end
