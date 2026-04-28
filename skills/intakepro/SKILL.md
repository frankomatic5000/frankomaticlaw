# ═══════════════════════════════════════════════════════════════
# SKILL: IntakePro — Customer Lead Capture & Management
# GrowBiz Media · OpenClaw AgentSkill · ClawHub-compatible
# ═══════════════════════════════════════════════════════════════

name: intakepro
version: "1.0.0"
description: >
  Customer intake and lead management for GrowBiz Media. Captures leads from
  Instagram DMs, phone calls (voice-to-text), and manual entries. Auto-qualifies,
  routes to appropriate agents, sends auto-replies, and tracks in CRM.
  Critical for revenue pipeline — urgency-based routing and immediate alerts.

author: frankomatic
license: MIT

# ═══════════════════════════════════════════════════════════════
# INPUTS
# ═══════════════════════════════════════════════════════════════

inputs:
  - name: source
    type: enum
    required: true
    options: [instagram_dm, phone_call, word_of_mouth, website_form, referral]
    description: Where the lead came from

  - name: prospect_name
    type: string
    required: true
    description: Lead's full name

  - name: contact_method
    type: enum
    required: true
    options: [instagram_handle, phone_number, email, whatsapp]
    description: How to reach them back

  - name: contact_value
    type: string
    required: true
    description: The actual contact info (handle, number, etc.)

  - name: service_interest
    type: enum
    required: true
    options: [
      growbiz_services_seo,
      growbiz_studio_video,
      growbiz_talks_speaking,
      growbiz_magazine_feature,
      imigrou_collaboration,
      general_inquiry,
      not_sure
    ]
    description: What service they're interested in

  - name: budget_hint
    type: enum
    required: false
    options: [under_500, 500_2000, 2000_5000, 5000_plus, not_discussed]
    default: not_discussed
    description: Budget range mentioned (if any)

  - name: urgency_signals
    type: array
    required: false
    description: Keywords indicating urgency ("ASAP", "urgent", "this week", etc.)

  - name: transcript
    type: string
    required: false
    description: Full conversation transcript (for DMs/calls)

  - name: captured_by
    type: enum
    required: true
    options: [jarbas, frank, frankcmo, manual_entry]
    description: Who captured this lead

# ═══════════════════════════════════════════════════════════════
# OUTPUTS
# ═══════════════════════════════════════════════════════════════

outputs:
  - name: lead_object
    type: object
    schema:
      lead_id: string              # LEAD-XXXX format
      status: enum[hot_warm_cold]
      score: integer                 # 0-100
      assigned_to: enum[frank, frankcmo, karine_via_jarbas]
      auto_reply_sent: boolean
      alert_triggered: boolean
      crm_logged: boolean
      follow_up_date: date
      notes: string

# ═══════════════════════════════════════════════════════════════
# LEAD SCORING LOGIC
# ═══════════════════════════════════════════════════════════════

logic:
  type: decision_tree
  
  scoring_rules:
    # Budget scoring
    - if budget_hint == "5000_plus": add 30 points
    - if budget_hint == "2000_5000": add 20 points
    - if budget_hint == "500_2000": add 10 points
    - if budget_hint == "under_500": add 5 points
    
    # Urgency scoring
    - if "urgent" in urgency_signals or "ASAP" in urgency_signals: add 25 points
    - if "this week" in urgency_signals or "tomorrow" in urgency_signals: add 15 points
    - if "next week" in urgency_signals: add 10 points
    
    # Service scoring (some are higher value)
    - if service_interest == "growbiz_services_seo": add 20 points
    - if service_interest == "growbiz_studio_video": add 15 points
    - if service_interest == "growbiz_talks_speaking": add 10 points
    
    # Source scoring
    - if source == "referral": add 15 points
    - if source == "phone_call": add 10 points (higher intent)
    
  status_calculation:
    - if score >= 70: status = "hot"
    - if score >= 40: status = "warm"
    - if score < 40: status = "cold"

# ═══════════════════════════════════════════════════════════════
# ROUTING LOGIC
# ═══════════════════════════════════════════════════════════════

  routing_rules:
    # GrowBiz Services (SEO) → FrankCMO
    - if service_interest == "growbiz_services_seo":
        assigned_to: frankcmo
        response_time: "within 2 hours"
    
    # Studios (Video production) → Karine/Jarbas for approval
    - if service_interest == "growbiz_studio_video":
        assigned_to: karine_via_jarbas
        response_time: "within 24 hours"
        note: "Karine must approve studio bookings"
    
    # Talks/Speaking → FrankCMO
    - if service_interest == "growbiz_talks_speaking":
        assigned_to: frankcmo
        response_time: "within 4 hours"
    
    # Magazine features → Frank (needs editorial review)
    - if service_interest == "growbiz_magazine_feature":
        assigned_to: frank
        response_time: "within 24 hours"
        note: "Editorial review required"
    
    # Imigrou collabs → Karine/Jarbas
    - if service_interest == "imigrou_collaboration":
        assigned_to: karine_via_jarbas
        response_time: "within 48 hours"
    
    # General inquiries → Frank (orchestrator decides)
    - if service_interest == "general_inquiry" or "not_sure":
        assigned_to: frank
        response_time: "within 4 hours"

# ═══════════════════════════════════════════════════════════════
# AUTO-REPLY TEMPLATES
# ═══════════════════════════════════════════════════════════════

  auto_reply_templates:
    # Instagram DM replies
    instagram_dm:
      growbiz_services_seo: |
        Obrigado pelo interesse nos serviços de SEO da GrowBiz! 
        
        Vamos analisar seu caso e retornamos em até 2 horas com próximos passos.
        
        — Equipe GrowBiz Services
      
      growbiz_studio_video: |
        Oi! Que legal que você quer trabalhar com a GrowBiz Studios 🎬
        
        Vou encaminhar para nossa equipe de produção. A Karine ou alguém da equipe vai entrar em contato em até 24h.
        
        — GrowBiz Studios
      
      default: |
        Obrigada pela mensagem! Recebemos seu contato e vamos retornar em breve.
        
        — GrowBiz Media
    
    # Phone call auto-reply (SMS/Email follow-up)
    phone_call:
      template: |
        Olá {prospect_name},
        
        Obrigado pela ligação de hoje! Conforme conversamos, estamos organizando as informações e você terá um retorno em {response_time}.
        
        Caso precise falar urgente, pode me ligar no mesmo número.
        
        Abraço,
        {assigned_agent_name}
        GrowBiz Media

# ═══════════════════════════════════════════════════════════════
# URGENCY ALERTS
# ═══════════════════════════════════════════════════════════════

  urgency_alerts:
    # IMMEDIATE ALERT (Hot leads $2000+)
    hot_lead_alert:
      trigger: score >= 70 OR budget_hint == "5000_plus"
      action: send_urgent_alert
      to: [frank, assigned_agent]
      message: "🚨 HOT LEAD: {prospect_name} | {service_interest} | {budget_hint} | Respond in {response_time}"
    
    # SPEAKING OPPORTUNITY (Urgent - time sensitive)
    speaking_urgent:
      trigger: service_interest == "growbiz_talks_speaking" AND urgency_signals contains "this month"
      action: send_urgent_alert
      to: [frank, frankcmo]
      message: "🎤 SPEAKING OPPORTUNITY: {prospect_name} | Event this month | Check availability ASAP"
    
    # STUDIO BOOKING (Karine needs to know)
    studio_booking:
      trigger: service_interest == "growbiz_studio_video"
      action: notify_jarbas_for_karine
      message: "🎬 STUDIO INQUIRY: {prospect_name} | Awaiting Karine's review"

# ═══════════════════════════════════════════════════════════════
# CRM INTEGRATION
# ═══════════════════════════════════════════════════════════════

  crm_logging:
    destination: "memory/intakepro/crm.jsonl"
    log_fields:
      - lead_id
      - timestamp
      - prospect_name
      - contact_method
      - contact_value
      - service_interest
      - score
      - status
      - assigned_to
      - source
      - captured_by
      - transcript (if available)

# ═══════════════════════════════════════════════════════════════
# ACCESS CONTROL
# ═══════════════════════════════════════════════════════════════

access_control:
  frank:
    allowed: [capture, view_all, reassign, update_status, export_crm]
    
  jarbas:
    allowed: [capture_via_instagram, view_assigned_to_karine, update_lead_status]
    note: "Jarbas captures Imigrou DMs and forwards studio inquiries to Karine"
    
  frankcmo:
    allowed: [view_services_leads, update_status, send_follow_up]
    note: "Owns SEO and Speaking lead follow-up"
    
  public_form:
    allowed: [submit_lead]
    note: "Website forms submit directly to IntakePro"

# ═══════════════════════════════════════════════════════════════
# TRIGGERS
# ═══════════════════════════════════════════════════════════════

triggers:
  - keyword: "new lead"
  - keyword: "prospect"
  - keyword: "interested in services"
  - keyword: "SEO inquiry"
  - keyword: "studio booking"
  - keyword: "speaking opportunity"
  - instagram_dm_received: true
  - phone_call_ended: true

# ═══════════════════════════════════════════════════════════════
# PERMISSIONS
# ═══════════════════════════════════════════════════════════════

permissions:
  - memory_read
  - memory_write
  - notify_channels
  - send_messages
  - create_tasks
  - read_calendar

preferred_model: kimi-k2.5:cloud
escalation_model: deepseek-chat

# ═══════════════════════════════════════════════════════════════
# NOTES
# ═══════════════════════════════════════════════════════════════

# - This skill is REVENUE-CRITICAL. Hot leads must never be dropped.
# - Auto-replies buy us time while we prepare personalized responses
# - CRM logging is append-only for audit trail
# - Karine must personally approve all studio bookings over $1000
# - FrankCMO handles all SEO inquiries (this is the cash cow)
