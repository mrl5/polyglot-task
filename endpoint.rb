#!/usr/bin/env ruby
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
puts "Your input:"

inp = gets.chomp
no_of_expressions = inp.to_i
if no_of_expressions.is_a? Integer
	if no_of_expressions > 0
		puts "Hurray"
	else
		abort("Number of RPN expressions must be greather than 0. Aborting.")
	end
else
	abort("First line must be an integer. Aborting.")
end
