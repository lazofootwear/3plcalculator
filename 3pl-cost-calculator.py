#!/usr/local/bin/python3

import sys
import math
import pandas as pd 

def isNaN(num):
   return num!= num

def percentage(part, whole):
  if whole == 0:
    return 0
  else:
    return float(part)/float(whole)

def calc_returns(vendor, return_rate, outboundunits):
  nri_returnflatfee=3.05
  nri_hourlyrate=45
  nri_minutesperbox=1

  lb_returnflatfee=5
  lb_hourlyrate=40
  lb_minutesperbox=2

  diy_cr_returns_per_hour=6
  diy_cr_hourly_wage=30
  
  
  numberofreturns=outboundunits*percentage(return_rate, 100)

  if vendor == 'NRI':
    return (numberofreturns*nri_returnflatfee+(nri_minutesperbox*numberofreturns/60*nri_hourlyrate))

  if vendor == 'LB':
    return (numberofreturns*lb_returnflatfee+(lb_minutesperbox*numberofreturns/60*lb_hourlyrate))

  if vendor == 'DIY':
    return (numberofreturns/diy_cr_returns_per_hour*diy_cr_hourly_wage)

def calc_receive(vendor, inboundunits, unitreceivecost, mixedskurepackcost, mixed_sku_percentage, totalinboundunits):
  realmixed_sku_percentage=percentage(mixed_sku_percentage, 100)
  repackcost=inboundunits*realmixed_sku_percentage*mixedskurepackcost
  subtotal=(inboundunits*unitreceivecost) + repackcost
  
  if vendor == 'LB':
    subtotal += 30
  
  if vendor == 'NRI':
    unitpercentage=percentage(inboundunits, totalinboundunits)
    subtotal += 10*unitpercentage

  return subtotal 

def calc_initialsetup(vendor):
  nri_initialsetup=8000
  lb_initialsetup=750
  diy_initialsetup=0
  if vendor == 'NRI':
    return nri_initialsetup    
  if vendor == 'LB':
    return lb_initialsetup    
  if vendor == 'DIY':
    return diy_initialsetup

def calc_monthlyfees(vendor):
  nri_monthlyfees=600
  lb_monthlyfees=35
  # for diy this is mostly inventory software fees
  diy_monthlyfees=1000
  if vendor == 'NRI':
    return nri_monthlyfees
  if vendor == 'LB':
    return lb_monthlyfees
  if vendor == 'DIY':
    return diy_monthlyfees

def print_stor(vendor, storagecostpercubicft):
  if vendor == 'NRI' or vendor == 'DIY':
    print("Storage Cost by Cubic Foot:" + storagecostpercubicft)
  else:
    print("Storage Cost by Cubic Foot:", '${:,.2f}'.format(storagecostpercubicft))
     
def calc_pickpack(vendor, onepickordercost, twopickordercost, outboundunits):
  yearly_labor_cost=float(250000)
  percent_of_one_item_orders=.80
  percent_of_two_item_orders=.20
  if vendor == 'DIY':
    return yearly_labor_cost/12/2
  else:
    return ((onepickordercost*outboundunits*percent_of_one_item_orders)+(twopickordercost*outboundunits*percent_of_two_item_orders))

def calc_storage(vendor, unitsonhand, outboundunits, storagecostpercubicft, type, bootsandshoesonhand):
  # shoe_cubicft 12.4” x 7.35” x 4.05”
  shoe_cubicft = .2136
 # boot_cubicft  12.4” x 9.84” x 4.05”
  boot_cubicft = .286 
  # average month has 30.4 days
  avg_days_per_month = 30.4
  nri_unit_threshhold = 10000
  nri_cost_after_threshhold = .30
  diy_yearly_storage_cost = 100000

  if vendor == 'NRI':
    if bootsandshoesonhand <= nri_unit_threshhold: 
      if bootsandshoesonhand == 0:
        return 1000/2
      else:
        return 1000 * (unitsonhand/bootsandshoesonhand)
    else:
      return (((bootsandshoesonhand - nri_unit_threshhold) * nri_cost_after_threshhold + 1000) * (unitsonhand/bootsandshoesonhand))
  elif vendor == 'LB' and type == 'shoes':
    return ((unitsonhand-(outboundunits/2)) * shoe_cubicft * storagecostpercubicft * avg_days_per_month)
  elif vendor == 'LB' and type == 'boots':
    return (unitsonhand-(outboundunits/2)* boot_cubicft * storagecostpercubicft * avg_days_per_month)
  elif vendor == 'DIY':
    return diy_yearly_storage_cost/12/2

def calc_coldstorage(vendor): 
    pricepersqft=1.55
    requiredsqft=4000/2
    # here is a little room to move around
    moveaboutroom=1.20
    gasfor20mi=50
    trunkrental=200
    labor=1000
    if vendor == 'NRI' or vendor == 'LB':
      return ((requiredsqft * pricepersqft * moveaboutroom) + gasfor20mi + trunkrental + labor)
    else:
      return 0

def calc_boxcosts(vendor, estimatedmonthlyorders, type):
  nri_one_lazo_shoe_box_cost=.39
  nri_two_lazo_shoe_box_stacked=.81
  nri_one_lazo_boot_box_cost=.49
  nri_two_lazo_boot_box_stacked=.81
  lb_one_lazo_shoe_box_cost=1.18
  lb_two_lazo_shoe_box_stacked=1.93
  lb_one_lazo_boot_box_cost=1.18
  lb_two_lazo_boot_box_stacked=1.93
  shop_one_lazo_shoe_box_cost=.83 #13"x9"x5" https://www.uline.com/Product/Detail/S-23955/Corrugated-Boxes-32-ECT/13-x-9-x-5-Lightweight-32-ECT-Corrugated-Boxes
  shop_two_lazo_shoe_box_stacked=.89 #14"x9"x9" https://www.uline.com/Product/Detail/S-23312/Corrugated-Boxes-32-ECT/14-x-9-x-9-Lightweight-32-ECT-Corrugated-Boxes
  #alt_shop_two_lazo_shoe_box_stacked=1.17 #or 13"x9"x9" (heavy duty) https://www.uline.com/Product/Detail/S-11373/Corrugated-Boxes-200-Test/13-x-9-x-9-Corrugated-Boxes
  shop_one_lazo_boot_box_cost=.86 #13"x10"x6" https://www.uline.com/Product/Detail/S-23310/Corrugated-Boxes-32-ECT/13-x-10-x-6-Lightweight-32-ECT-Corrugated-Boxes
  #alt_shop_one_lazo_boot_box_cost=1.01 #or 14"x10"x5" (heavy duty) https://www.uline.com/Product/Detail/S-4986/Corrugated-Boxes-200-Test/14-x-10-x-5-Corrugated-Boxes
  shop_two_lazo_boot_box_stacked=1.06 #13"x10"x10" https://www.uline.com/Product/Detail/S-21571/Corrugated-Boxes-32-ECT/13-x-10-x-10-Lightweight-32-ECT-Corrugated-Boxes

  percent_of_one_item_orders=.80
  percent_of_two_item_orders=.20
 
  if vendor == 'NRI' and type == 'shoes':
    return ((estimatedmonthlyorders*percent_of_one_item_orders*nri_one_lazo_shoe_box_cost) + (estimatedmonthlyorders*percent_of_two_item_orders*nri_two_lazo_shoe_box_stacked))
  elif vendor == 'NRI' and type == 'boots':
    return ((estimatedmonthlyorders*percent_of_one_item_orders*nri_one_lazo_boot_box_cost) + (estimatedmonthlyorders*percent_of_two_item_orders*nri_two_lazo_boot_box_stacked))
  elif vendor == 'LB' and type == 'shoes':
    return ((estimatedmonthlyorders*percent_of_one_item_orders*lb_one_lazo_shoe_box_cost) + (estimatedmonthlyorders*percent_of_two_item_orders*lb_two_lazo_shoe_box_stacked))
  elif vendor == 'LB' and type == 'boots':
    return ((estimatedmonthlyorders*percent_of_one_item_orders*lb_one_lazo_boot_box_cost) + (estimatedmonthlyorders*percent_of_two_item_orders*lb_two_lazo_boot_box_stacked))
  elif vendor == 'DIY' and type == 'shoes':
    return ((estimatedmonthlyorders*percent_of_one_item_orders*shop_one_lazo_shoe_box_cost) + (estimatedmonthlyorders*percent_of_two_item_orders*shop_two_lazo_shoe_box_stacked))
  elif vendor == 'DIY' and type == 'boots':
    return ((estimatedmonthlyorders*percent_of_one_item_orders*shop_one_lazo_boot_box_cost) + (estimatedmonthlyorders*percent_of_two_item_orders*shop_two_lazo_boot_box_stacked))

def calc_shipping(vendor, monthlyorders, type):
  nri_one_lazo_shoe_shipping_cost=8.01
  nri_two_lazo_shoe_shipping_cost=8.20
  nri_one_lazo_boot_shipping_cost=8.18
  nri_two_lazo_boot_shipping_cost=8.32
  lb_one_lazo_shoe_shipping_cost=15.10
  lb_two_lazo_shoe_shipping_cost=17.22
  lb_one_lazo_boot_shipping_cost=15.67
  lb_two_lazo_boot_shipping_cost=17.22
  shop_one_lazo_shoe_shipping_cost=10.10
  shop_two_lazo_shoe_shipping_cost=11.44
  shop_one_lazo_boot_shipping_cost=10.59
  shop_two_lazo_boot_shipping_cost=11.87

  percent_of_diy_over_shop_rates=1.03

  percent_of_one_item_orders=.80
  percent_of_two_item_orders=.20

  if vendor == 'NRI' and type == 'shoes':
    return ((monthlyorders*percent_of_one_item_orders*nri_one_lazo_shoe_shipping_cost) + (monthlyorders*percent_of_two_item_orders*nri_two_lazo_shoe_shipping_cost))
  if vendor == 'NRI' and type == 'boots':
    return ((monthlyorders*percent_of_one_item_orders*nri_one_lazo_boot_shipping_cost) + (monthlyorders*percent_of_two_item_orders*nri_two_lazo_boot_shipping_cost))
  if vendor == 'LB' and type == 'shoes':
    return ((monthlyorders*percent_of_one_item_orders*lb_one_lazo_shoe_shipping_cost) + (monthlyorders*percent_of_two_item_orders*lb_two_lazo_shoe_shipping_cost))
  if vendor == 'LB' and type == 'boots':
    return ((monthlyorders*percent_of_one_item_orders*lb_one_lazo_boot_shipping_cost) + (monthlyorders*percent_of_two_item_orders*lb_two_lazo_boot_shipping_cost))
  if vendor == 'DIY' and type == 'shoes':
    return ((monthlyorders*percent_of_one_item_orders*shop_one_lazo_shoe_shipping_cost) + (monthlyorders*percent_of_two_item_orders*shop_two_lazo_shoe_shipping_cost))*percent_of_diy_over_shop_rates
  if vendor == 'DIY' and type == 'boots':
    return ((monthlyorders*percent_of_one_item_orders*shop_one_lazo_boot_shipping_cost) + (monthlyorders*percent_of_two_item_orders*shop_two_lazo_boot_shipping_cost))*percent_of_diy_over_shop_rates

# start of main  
args_list = sys.argv
del args_list[0]
plname=(args_list[0])
filecsv=(args_list[1])
df = pd.read_csv(filecsv, low_memory=False)

yearly_cost=0
total_initialsetup_cost=0
total_outbound_sneakers=0
total_outbound_boots=0
total_admin_cost=0
total_pickpack_cost=0
total_box_boot_cost=0
total_box_shoe_cost=0
total_storage_cost=0
total_receive_cost=0
total_postage_boots=0
total_postage_shoes=0
total_cold_storage_cost=0
total_returns_cost=0
averageordersize=float(1.2)
mixed_sku_percentage=10
sneakers_on_hand=int(0)
boots_on_hand=int(0)
total_cost=int(0)
msrp_sneaker=120
msrp_boot=200
return_rate=15

if plname == 'DIY':
   onboarding_cost=int(0)
   shoereceivecost=float(0)
   bootreceivecost=float(0)
   onepickordercost=float(0)
   twopickordercost=float(0)
   threepickordercost=float(0)
   mixedskurepackcost=float(0)
   admin_cost=int(0)
   storagecostpercubicft='FIXED $8333/mo'
if plname == 'NRI':
   onboarding_cost=int(8000)
   shoereceivecost=float(.22)
   bootreceivecost=float(.22)
   onepickordercost=float(3.00)
   twopickordercost=float(3.75)
   threepickordercost=float(4.50)
   mixedskurepackcost=float(.18)
   admin_cost=int(600)
   storagecostpercubicft='FIXED $1000/mo up to 10K units. $.30/unit therafter'
elif plname == 'LB':
   onboarding_cost=int(500)
   shoereceivecost=float(.20)
   bootreceivecost=float(.166)
   onepickordercost=float(3.50)
   twopickordercost=float(3.50)
   threepickordercost=float(4.00)
   mixedskurepackcost=float(.20) #estimate
   admin_cost=int(35)
   storagecostpercubicft=float(.04)

print("3PL Name:", plname)
print("Mixed SKU Percentage:", mixed_sku_percentage,"%")
print("Mixed SKU Repack Cost:", '${:,.2f}'.format(mixedskurepackcost))
print("Shoe Unit Receive Cost:", '${:,.2f}'.format(shoereceivecost))
print("Boot Unit Receive Cost:", '${:,.2f}'.format(bootreceivecost))
print("Average Order Size:", averageordersize, "Units")
print("Order With One Pick Cost:", '${:,.2f}'.format(onepickordercost))
print("Order With Two Pick Cost:", '${:,.2f}'.format(twopickordercost))
print("Order With Three Pick Cost:", '${:,.2f}'.format(threepickordercost))
print_stor(plname, storagecostpercubicft)
print("MSRP sneaker:", '${:,.2f}'.format(msrp_sneaker))
print("MSRP boot:", '${:,.2f}'.format(msrp_boot))
print("Return Rate:", '{:,.2f}'.format(return_rate), "%")

print("")
print("")


for index, row in df.iterrows():
  # pull data from csv
  month=row['month'] 
  # if cells are empty in csv, make them 0
  if not isNaN(row['inbound_sneakers']):
    inbound_sneakers = row['inbound_sneakers']
  else:
    inbound_sneakers = 0

  if not isNaN(row['inbound_boots']):
    inbound_boots = row['inbound_boots']
  else:
    inbound_boots = 0

  if not isNaN(row['outbound_sneakers']):
    outbound_sneakers = row['outbound_sneakers']
  else:
    outbound_sneakers = 0

  if not isNaN(row['outbound_boots']):
    outbound_boots = row['outbound_boots']
  else:
    outbound_boots = 0
  print("Data for Month:", month)
  #keep a tally of current shoes and boots on hand 
  print("Inbound Sneakers:",inbound_sneakers)
  print("Inbound Boots:",inbound_boots)
  sneakers_on_hand += inbound_sneakers
  boots_on_hand += inbound_boots
  print("Sneakers On-hand after any Receiving:", sneakers_on_hand)
  print("Boots On-hand after any Receiving:", boots_on_hand)
  print("Outbound Sneakers to Customers:",outbound_sneakers)
  print("Outbound Boots to Customers:",outbound_boots)

  monthly_fees=calc_monthlyfees(plname)
  print("Various Monthly Fees (Software/Admin):", '${:,.2f}'.format(monthly_fees))


### SHOES
  shoe_receive_cost = calc_receive(plname, inbound_sneakers, shoereceivecost, mixedskurepackcost, mixed_sku_percentage, inbound_sneakers+inbound_boots)

  if sneakers_on_hand >= outbound_sneakers:
    shoe_pick_pack_cost = calc_pickpack(plname, onepickordercost, twopickordercost, outbound_sneakers)
    shoe_box_cost = calc_boxcosts(plname, outbound_sneakers, "shoes")
    shoe_storage_cost = calc_storage(plname, sneakers_on_hand, outbound_sneakers, storagecostpercubicft, "shoes", sneakers_on_hand + boots_on_hand)
    shoe_shipping_cost = calc_shipping(plname, outbound_sneakers, "shoes")
    shoe_returns_cost = calc_returns(plname, return_rate, outbound_sneakers)
  else:
    shoe_pick_pack_cost = calc_pickpack(plname, onepickordercost, twopickordercost, sneakers_on_hand)
    shoe_box_cost = calc_boxcosts(plname, sneakers_on_hand, "shoes")
    shoe_storage_cost = calc_storage(plname, outbound_sneakers, outbound_sneakers, storagecostpercubicft, "shoes", outbound_sneakers + boots_on_hand)
    shoe_shipping_cost = calc_shipping(plname, sneakers_on_hand, "shoes")
    shoe_returns_cost = calc_returns(plname, return_rate, sneakers_on_hand)

### BOOTS
  boot_receive_cost = calc_receive(plname, inbound_boots, bootreceivecost, mixedskurepackcost, mixed_sku_percentage, inbound_sneakers+inbound_boots)

  if boots_on_hand >= outbound_boots:
    boot_pick_pack_cost = calc_pickpack(plname, onepickordercost, twopickordercost, outbound_boots)
    boot_box_cost = calc_boxcosts(plname, outbound_boots, "boots")
    boot_storage_cost = calc_storage(plname, boots_on_hand, outbound_boots, storagecostpercubicft, "boots",  boots_on_hand + sneakers_on_hand)
    boot_shipping_cost = calc_shipping(plname, outbound_boots, "boots")
    boot_returns_cost = calc_returns(plname, return_rate, outbound_boots)
  else:
    boot_pick_pack_cost = calc_pickpack(plname, onepickordercost, twopickordercost, boots_on_hand)
    boot_box_cost = calc_boxcosts(plname, boots_on_hand, "boots")
    boot_storage_cost = calc_storage(plname, outbound_boots, outbound_boots, storagecostpercubicft, "boots", outbound_boots + sneakers_on_hand)
    boot_shipping_cost = calc_shipping(plname, boots_on_hand, "boots")
    boot_returns_cost = calc_returns(plname, return_rate, boots_on_hand)

  if month == 1:
    initialsetup_cost=calc_initialsetup(plname)
    total_initialsetup_cost=initialsetup_cost
    print("One Time Setup Cost:", '${:,.2f}'.format(initialsetup_cost))
  else:
    initialsetup_cost=0

  #tally monthy admin fees
  total_admin_cost+=monthly_fees

  # tally receive cost
  total_receive_cost+=(shoe_receive_cost+boot_receive_cost)

  # tally pick/pack cost
  total_pickpack_cost+=(shoe_pick_pack_cost+boot_pick_pack_cost)
  
  # tally box cost
  total_box_shoe_cost+=shoe_box_cost
  total_box_boot_cost+=boot_box_cost

  # tally storage cost
  total_storage_cost+=(shoe_storage_cost+boot_storage_cost)

  #tally postage cost
  total_postage_boots+=boot_shipping_cost
  total_postage_shoes+=shoe_shipping_cost

  cold_storage_cost = calc_coldstorage(plname)

  #tally cold storage cost
  total_cold_storage_cost+=cold_storage_cost

  #tally total returns cost
  total_returns_cost+=(shoe_returns_cost+boot_returns_cost)

  print("Sneaker Receiving Cost:", '${:,.2f}'.format(shoe_receive_cost))
  print("Sneaker Pick/Pack Cost:", '${:,.2f}'.format(shoe_pick_pack_cost))
  print("Sneaker Cardboard Shipping Box Cost:", '${:,.2f}'.format(shoe_box_cost))
  print("Sneaker Storage Cost:", '${:,.2f}'.format(shoe_storage_cost))
  print("Sneaker Postage Cost:", '${:,.2f}'.format(shoe_shipping_cost))
  print("Sneaker Returns Cost:", '${:,.2f}'.format(shoe_returns_cost))
  print("Cold Storage, Truck Rental, Gas and Labor Cost (if reqd):", '${:,.2f}'.format(cold_storage_cost))
  print("Boot Receiving Cost:", '${:,.2f}'.format(boot_receive_cost))
  print("Boot Pick/Pack Cost:", '${:,.2f}'.format(boot_pick_pack_cost))
  print("Boot Cardboard Shipping Box Cost:", '${:,.2f}'.format(boot_box_cost))
  print("Boot Storage Cost:", '${:,.2f}'.format(boot_storage_cost))
  print("Boot Postage Cost:", '${:,.2f}'.format(boot_shipping_cost))
  print("Boot Returns Cost:", '${:,.2f}'.format(boot_returns_cost))

  total_outbound_sneakers += outbound_sneakers 
  print("total_outbound_sneakers:", total_outbound_sneakers)
  total_outbound_boots += outbound_boots
  print("total_outbound_boots:", total_outbound_boots)

  sneakers_on_hand-=outbound_sneakers
  if sneakers_on_hand <= 0:
    sneakers_on_hand=0

  boots_on_hand-=outbound_boots
  if boots_on_hand <= 0:
    boots_on_hand=0

  print("Sneakers On-hand at end of Month:", sneakers_on_hand)
  print("Boots On-hand at end of Month:", boots_on_hand)
  
  monthly_cost=monthly_fees+shoe_receive_cost+shoe_pick_pack_cost+shoe_box_cost+shoe_storage_cost+shoe_shipping_cost+shoe_returns_cost+boot_receive_cost+boot_pick_pack_cost+boot_box_cost+boot_storage_cost+boot_shipping_cost+boot_returns_cost+initialsetup_cost+cold_storage_cost
  yearly_cost += monthly_cost
  print("Monthly Cost:", '${:,.2f}'.format(monthly_cost))
  print("")

print("Total Initial Setup Fees:", '${:,.2f}'.format(total_initialsetup_cost))
print("Total Monthly Fees (Software/Admin):", '${:,.2f}'.format(total_admin_cost))
print("Total Receiving Cost:", '${:,.2f}'.format(total_receive_cost))
print("Total Pick/Pack Cost:", '${:,.2f}'.format(total_pickpack_cost))
print("Total Sneaker Cardboard Box Cost:", '${:,.2f}'.format(total_box_shoe_cost))
print("Total Boot Cardboard Box Cost:", '${:,.2f}'.format(total_box_boot_cost))
print("--Total Cardboard Box Cost:", '${:,.2f}'.format(total_box_shoe_cost+total_box_boot_cost))
print("Total Storage Cost:", '${:,.2f}'.format(total_storage_cost))
print("Total Sneaker Postage Cost:", '${:,.2f}'.format(total_postage_shoes))
print("Total Boot Postage Cost:", '${:,.2f}'.format(total_postage_boots))
print("--Total Postage Cost:", '${:,.2f}'.format(total_postage_shoes+total_postage_boots))
print("Total Cold Storage Cost:", '${:,.2f}'.format(total_cold_storage_cost))
print("Total Returns Processing:", '${:,.2f}'.format(total_returns_cost))
print("Total Yearly Cost:", '${:,.2f}'.format(yearly_cost))
print("Total Shipped Sneakers", total_outbound_sneakers, "totaling", '${:,.2f}'.format(total_outbound_sneakers*msrp_sneaker), "in Revenue.") 
print("Total Shipped Boots", total_outbound_boots, "totaling", '${:,.2f}'.format(total_outbound_boots*msrp_boot), "in Revenue.") 
print("Total Shipped Units", (total_outbound_sneakers+total_outbound_boots), "totaling", '${:,.2f}'.format(total_outbound_boots*msrp_boot+total_outbound_sneakers*msrp_sneaker), "in Revenue")
print("Total Fufillment Cost (not including postage) as a % of Total Revenue", '{:,.2f}'.format((yearly_cost-(total_postage_shoes+total_postage_boots))/(total_outbound_boots*msrp_boot+total_outbound_sneakers*msrp_sneaker)*100),"%") 
print("Total Fufillment Cost as a % of Total Revenue", '{:,.2f}'.format(yearly_cost/(total_outbound_boots*msrp_boot+total_outbound_sneakers*msrp_sneaker)*100),"%") 
