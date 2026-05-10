#!/usr/bin/env python3
"""
AI Receptionist Demo - Interactive demonstration of the AI receptionist system
"""

from ai_receptionist import AIReceptionist, create_sample_clients
import time


def print_banner():
    """Print the demo banner"""
    print("🤖" + "=" * 60 + "🤖")
    print("           AI RECEPTIONIST BUSINESS DEMO")
    print("    Starting an Online Business with AI: A Modern Approach")
    print("🤖" + "=" * 60 + "🤖")
    print()


def print_business_model():
    """Print the business model information"""
    print("💰 BUSINESS MODEL OVERVIEW")
    print("-" * 30)
    print("• Target: Small Local Businesses (Dentists, Electricians, Hair Salons)")
    print("• Service: 24/7 AI Voice Agent for Answering Calls")
    print("• Revenue: $300-$500/month per client")
    print("• Features: Appointment Booking, Lead Capture, Customer Service")
    print("• Scalability: Multiple clients, recurring income")
    print()


def simulate_business_scenarios():
    """Simulate real business scenarios"""
    print("🎭 BUSINESS SCENARIO SIMULATIONS")
    print("-" * 35)

    # Initialize the system
    receptionist = AIReceptionist()

    # Add sample clients
    sample_clients = create_sample_clients()
    for client in sample_clients:
        receptionist.add_client(client)

    scenarios = [
        {
            "title": "Dental Practice - Emergency Call",
            "client_id": "dental_001",
            "caller_message": "Hi, I have a terrible toothache and need to see a dentist today. It's really painful!",
            "expected_outcome": "Emergency appointment booking",
        },
        {
            "title": "Hair Salon - Appointment Booking",
            "client_id": "salon_001",
            "caller_message": "I'd like to book a haircut and highlights for next week. What do you have available?",
            "expected_outcome": "Service consultation and booking",
        },
        {
            "title": "Electrician - Service Inquiry",
            "client_id": "electric_001",
            "caller_message": "My lights keep flickering and I'm worried about electrical safety. Can someone come check it out?",
            "expected_outcome": "Safety concern addressed, service scheduled",
        },
    ]

    for i, scenario in enumerate(scenarios, 1):
        print(f"\n📞 Scenario {i}: {scenario['title']}")
        print("-" * 50)

        client = receptionist.get_client(scenario["client_id"])
        if not client:
            print("❌ Client not found")
            continue

        print(f"🏢 Business: {client.name}")
        print(f"📞 Caller: {scenario['caller_message']}")
        print(f"🎯 Expected: {scenario['expected_outcome']}")

        print("\n🤖 AI Response:")
        print("-" * 20)

        response = receptionist.generate_ai_response(client, scenario["caller_message"])
        print(response)

        # Log the call
        receptionist.log_call(
            client_id=client.id,
            caller_phone="+1-555-0000",
            call_duration=120,
            outcome="appointment_booked"
            if "appointment" in response.lower()
            else "lead_captured",
            transcript=f"Caller: {scenario['caller_message']}\nAI: {response}",
        )

        print("\n✅ Call logged and processed!")
        time.sleep(1)


def demonstrate_features():
    """Demonstrate key features of the system"""
    print("\n🔧 SYSTEM FEATURES DEMONSTRATION")
    print("-" * 35)

    receptionist = AIReceptionist()

    # Show client management
    print("\n1. 📋 CLIENT MANAGEMENT")
    print("-" * 25)
    clients = ["dental_001", "salon_001", "electric_001"]
    for client_id in clients:
        client = receptionist.get_client(client_id)
        if client:
            print(f"• {client.name} ({client.industry}) - ${client.monthly_fee}/month")

    # Show appointment booking
    print("\n2. 📅 APPOINTMENT BOOKING")
    print("-" * 25)
    client = receptionist.get_client("dental_001")
    if client:
        success = receptionist.book_appointment(
            client_id=client.id,
            customer_name="John Smith",
            customer_phone="+1-555-1234",
            service="General Cleaning",
            appointment_date="2024-11-15",
            appointment_time="10:00 AM",
            notes="Regular checkup",
        )
        if success:
            print(
                "✅ Appointment booked: John Smith - General Cleaning - Nov 15, 10:00 AM"
            )

    # Show analytics
    print("\n3. 📊 ANALYTICS & REPORTING")
    print("-" * 25)
    analytics = receptionist.get_business_analytics("dental_001", 30)
    print(f"• Total Calls: {analytics.get('total_calls', 0)}")
    print(f"• Appointments Booked: {analytics.get('appointments_booked', 0)}")
    print(f"• Conversion Rate: {analytics.get('conversion_rate', 0)}%")


def show_revenue_calculation():
    """Show potential revenue calculations"""
    print("\n💰 REVENUE PROJECTION CALCULATOR")
    print("-" * 35)

    # Pricing tiers

    # Client scenarios
    scenarios = [
        {"name": "Conservative", "clients": 10, "avg_price": 350},
        {"name": "Moderate", "clients": 25, "avg_price": 400},
        {"name": "Aggressive", "clients": 50, "avg_price": 450},
    ]

    print("Monthly Revenue Projections:")
    print("-" * 30)

    for scenario in scenarios:
        monthly_revenue = scenario["clients"] * scenario["avg_price"]
        annual_revenue = monthly_revenue * 12

        print(f"\n{scenario['name']} Growth:")
        print(f"  • Clients: {scenario['clients']}")
        print(f"  • Avg Price: ${scenario['avg_price']}")
        print(f"  • Monthly Revenue: ${monthly_revenue:,}")
        print(f"  • Annual Revenue: ${annual_revenue:,}")

    print("\n💡 Break-even Analysis:")
    print("  • Break-even: 1-2 clients (covers basic costs)")
    print("  • Profitable: 3+ clients")
    print("  • Scale target: 10+ clients")


def interactive_demo():
    """Run interactive demo"""
    print("\n🎮 INTERACTIVE DEMO")
    print("-" * 20)

    receptionist = AIReceptionist()

    # Add sample clients
    sample_clients = create_sample_clients()
    for client in sample_clients:
        receptionist.add_client(client)

    while True:
        print("\nChoose a demo option:")
        print("1. Simulate a call")
        print("2. Book an appointment")
        print("3. View analytics")
        print("4. Add new client")
        print("5. Exit demo")

        choice = input("\nEnter choice (1-5): ").strip()

        if choice == "1":
            simulate_interactive_call(receptionist)
        elif choice == "2":
            book_interactive_appointment(receptionist)
        elif choice == "3":
            view_interactive_analytics(receptionist)
        elif choice == "4":
            add_interactive_client(receptionist)
        elif choice == "5":
            print("👋 Thanks for trying the AI Receptionist demo!")
            break
        else:
            print("❌ Invalid choice. Please try again.")


def simulate_interactive_call(receptionist):
    """Interactive call simulation"""
    print("\n📞 CALL SIMULATION")
    print("-" * 20)

    clients = []
    for client_id in ["dental_001", "salon_001", "electric_001"]:
        client = receptionist.get_client(client_id)
        if client:
            clients.append(client)

    print("Available businesses:")
    for i, client in enumerate(clients, 1):
        print(f"{i}. {client.name} ({client.industry})")

    try:
        choice = int(input("\nSelect business (1-{}): ".format(len(clients)))) - 1
        if 0 <= choice < len(clients):
            client = clients[choice]
            print(f"\n📞 Calling {client.name}...")

            caller_message = input("\nWhat would you like to say? ")

            print("\n🤖 AI Receptionist:")
            print("-" * 25)
            response = receptionist.generate_ai_response(client, caller_message)
            print(response)

            # Log the call
            receptionist.log_call(
                client_id=client.id,
                caller_phone="+1-555-0000",
                call_duration=60,
                outcome="lead_captured",
                transcript=f"Caller: {caller_message}\nAI: {response}",
            )
        else:
            print("❌ Invalid selection.")
    except ValueError:
        print("❌ Please enter a valid number.")


def book_interactive_appointment(receptionist):
    """Interactive appointment booking"""
    print("\n📅 BOOK APPOINTMENT")
    print("-" * 20)

    client_id = input("Enter client ID (dental_001, salon_001, electric_001): ").strip()
    client = receptionist.get_client(client_id)

    if not client:
        print("❌ Client not found.")
        return

    print(f"\nBooking for {client.name}")
    print(f"Services: {', '.join(client.services)}")

    customer_name = input("Customer name: ").strip()
    customer_phone = input("Customer phone: ").strip()
    service = input("Service: ").strip()
    appointment_date = input("Date (YYYY-MM-DD): ").strip()
    appointment_time = input("Time (HH:MM): ").strip()

    if receptionist.book_appointment(
        client_id,
        customer_name,
        customer_phone,
        service,
        appointment_date,
        appointment_time,
    ):
        print("✅ Appointment booked successfully!")
    else:
        print("❌ Failed to book appointment.")


def view_interactive_analytics(receptionist):
    """Interactive analytics viewing"""
    print("\n📊 ANALYTICS")
    print("-" * 15)

    client_id = input("Enter client ID: ").strip()
    client = receptionist.get_client(client_id)

    if not client:
        print("❌ Client not found.")
        return

    analytics = receptionist.get_business_analytics(client_id, 30)

    print(f"\n📈 {client.name} - Last 30 Days")
    print(f"Total Calls: {analytics.get('total_calls', 0)}")
    print(f"Appointments Booked: {analytics.get('appointments_booked', 0)}")
    print(f"Conversion Rate: {analytics.get('conversion_rate', 0)}%")


def add_interactive_client(receptionist):
    """Interactive client addition"""
    print("\n➕ ADD NEW CLIENT")
    print("-" * 20)
    print("This would open a form to add a new business client.")
    print("For now, using sample clients only.")
    print("✅ Sample clients are already loaded!")


def main():
    """Main demo function"""
    print_banner()
    print_business_model()

    print("🚀 Starting AI Receptionist Demo...")
    print()

    # Run demonstrations
    simulate_business_scenarios()
    demonstrate_features()
    show_revenue_calculation()

    # Interactive demo
    print("\n" + "=" * 60)
    print("Ready for interactive demo? (y/n)")
    if input().lower().startswith("y"):
        interactive_demo()

    print("\n🎉 Demo completed!")
    print("This AI Receptionist system is ready for real business implementation!")


if __name__ == "__main__":
    main()
