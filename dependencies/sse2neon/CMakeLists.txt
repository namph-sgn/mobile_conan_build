add_library(sse2neon INTERFACE) # giống proxy, có thể include nhiều thư viện chung

target_include_directories(sse2neon INTERFACE ${CMAKE_CURRENT_SOURCE_DIR}) # Private: thư viện cần include phải link