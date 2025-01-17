rule example_rule {
    meta:
        author = "John Doe"
        description = "Detects example pattern"
        date = "2025-01-17"
        version = "1.0"

    strings:
        $text_string = "example"
        $hex_string = { 01 02 03 }

    condition:
        any of them
}