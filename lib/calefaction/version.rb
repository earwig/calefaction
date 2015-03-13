module Calefaction::Version
  MAJOR   = 0
  MINOR   = 1
  PATCH   = 0
  RELEASE = false
  VERSION_STRING = "#{MAJOR}.#{MINOR}.#{PATCH}#{"-dev" unless RELEASE}"
end
