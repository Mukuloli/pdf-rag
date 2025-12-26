"""
Test script to verify text formatting functionality.
"""
from utils.text_formatter import format_response_text


def test_spacing_fix():
    """Test the text formatter with the example provided by the user."""
    
    # Original text with spacing issues
    original_text = """T he TCP 3-Way Handshake is a fundamentalprocess in establishing a reliableconnect i on be tween two devices over a net work. During t h is handshake, the in i tiating device (let's c a ll it Device A)sends a SYN (synchronize) packet to the re ceiving device (Device B) to start t he connect i on set up. Device Bresponds with a SYN-ACK (synchronize-acknowledgment)packet to a cknowledge the re quest a nd signal i ts readiness to establish the connect i on. Finally,Device As ends an A CK (acknowledgment)packet back to Device Btoconfirm the connect i on establishment. T h is-way exchangeensures that both devices a gree on t he in i tial sequence numbers f or dat a transmiss i on a nd confirms th at both parties a re ready to communicate. It's like a politeconversat i on w he re each sideintroduces them selves a nd confirms they a re ready to start talking. In t he context provided,t he TCP/IP modelcombines the presentat i on a nd sess i on layers in to i ts a pplicat i on layer, simplifying t he protocol stack compared to t he OS I model. TCP/IP's transport layer,especially when us i ng UDP, may not a lways guarantee reliablepacket deliverylike t he OS I model do es with i ts transportlayer protocols. Understanding t he TCP-Way Handshake is crucial f or ensuringsuccessful a nd reliable communicat i on be tween devices in a net work."""
    
    # Apply formatting
    formatted_text = format_response_text(original_text)
    
    print("=" * 80)
    print("ORIGINAL TEXT (with spacing issues):")
    print("=" * 80)
    print(original_text)
    print("\n" + "=" * 80)
    print("FORMATTED TEXT (spacing fixed):")
    print("=" * 80)
    print(formatted_text)
    print("\n" + "=" * 80)
    
    # Check for common issues that should be fixed
    issues_to_check = [
        ("connect i on", "connection"),
        ("be tween", "between"),
        ("T h is", "This"),
        ("t he", "the"),
        ("a nd", "and"),
        ("w he re", "where"),
        ("i n", "in"),
        ("f or", "for"),
    ]
    
    print("\nCHECKING SPECIFIC FIXES:")
    print("=" * 80)
    for issue, expected_fix in issues_to_check:
        if issue in original_text:
            is_fixed = issue not in formatted_text
            status = "✓ FIXED" if is_fixed else "✗ NOT FIXED"
            print(f"{status}: '{issue}' -> '{expected_fix}'")
    
    print("\n" + "=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    test_spacing_fix()
